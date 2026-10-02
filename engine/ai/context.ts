import type { FrameSource } from '../served';
import type { SubjectHead } from '../model';
import type { AskContext } from './provider';

/**
 * The ask context for a frame, built on the server from the subject it
 * serves (its head, and the frame's reading and citations from the
 * library): the client names a frame and trail, never their content. Null when
 * the frame is unknown, or the trail is unknown or does not hold the frame.
 */
export function askContext(
	subject: SubjectHead,
	frameId: unknown,
	trailId: unknown,
	{ reading, citations }: FrameSource
): AskContext | null {
	if (typeof frameId !== 'string' || !Object.hasOwn(subject.frames, frameId)) return null;
	const trail =
		trailId === null || trailId === undefined
			? null
			: (subject.trails.find((t) => t.id === trailId) ?? undefined);
	if (trail === undefined) return null;
	const segment = (trail ? trail.spine : subject.spine).segments.find((s) =>
		s.frames.includes(frameId)
	);
	if (!segment) return null;
	const frame = subject.frames[frameId];
	return {
		subject: { title: subject.title },
		frame: {
			id: frameId,
			title: `${frame.scene.headline} ${frame.scene.accent}`,
			position: frame.position.label,
			segment: segment.title,
			reading,
			...(frame.asOf ? { asOf: frame.asOf } : {}),
			citations
		},
		trail: trail ? { id: trail.id, title: trail.title } : null
	};
}
