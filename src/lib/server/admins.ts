import type { DatabaseSync } from 'node:sqlite';

/**
 * The site's admins (docs/design.md §Traffic, korg 3570): readers who may see
 * the traffic page, kept by login in `reader.db`'s `admin` table (the
 * store's migration 9) and given or taken only by `admin.mjs admin`. Like
 * the ask ledger it imports nothing but `node:` modules and types, so the
 * admin CLI loads it with plain Node.
 */

export interface Admin {
	reader: string;
	enabled: string;
}

export interface Admins {
	is(reader: string | null | undefined): boolean;
	enable(reader: string, now?: Date): Admin;
	disable(reader: string): boolean;
	list(): Admin[];
}

export function openAdmins(db: DatabaseSync): Admins {
	const get = db.prepare('SELECT reader, enabled FROM admin WHERE reader = ?');
	const put = db.prepare(
		'INSERT INTO admin (reader, enabled) VALUES (?, ?) ON CONFLICT (reader) DO NOTHING'
	);
	const drop = db.prepare('DELETE FROM admin WHERE reader = ?');
	const all = db.prepare('SELECT reader, enabled FROM admin ORDER BY reader');
	const admin = (r: unknown) => ({ ...(r as Admin) });
	return {
		is: (reader) => !!reader && !!get.get(reader),
		enable(reader, now = new Date()) {
			put.run(reader, now.toISOString());
			return admin(get.get(reader));
		},
		disable: (reader) => drop.run(reader).changes > 0,
		list: () => all.all().map(admin)
	};
}
