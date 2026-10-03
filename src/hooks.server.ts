// Who may read and write, and what starts with the server, are the
// edition's (docs/deploying.md §Editions): the full edition's doors on kai
// (src/lib/edition/full/hooks.ts), or the reader edition's sign-in
// (src/lib/edition/reader/hooks.ts).
export { handle, init } from '$edition/hooks';
