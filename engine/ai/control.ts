import { ASK_MODEL, GROW_MODEL } from '../settings';
import type { GrowVerb } from './grow';

/**
 * The AI pane's one control (docs/design.md §The AI control, korg 3411): a
 * verb, a text box and a send button. "Ask a question" comes first and is the
 * default; grow's verbs follow when the app config offers grow. The verb
 * decides the button's word, the placeholder and which model setting applies.
 */
export type AiVerb = 'ask' | GrowVerb;

export interface VerbOption {
	value: AiVerb;
	label: string;
	placeholder: string;
	/** The send button's word. */
	send: 'Ask' | 'Grow';
	/** The setting id of the model it runs on. */
	model: string;
}

const ASK: VerbOption = {
	value: 'ask',
	label: 'Ask a question',
	placeholder: 'Ask about what you are reading…',
	send: 'Ask',
	model: ASK_MODEL
};

const GROW: VerbOption[] = [
	{
		value: 'frames',
		label: 'Grow: new frames on the main spine',
		placeholder: 'What the main story should add…'
	},
	{
		value: 'trail',
		label: 'Grow: a side trail from this frame',
		placeholder: 'What the side trail should follow…'
	},
	{
		value: 'both',
		label: 'Grow: a new frame with its own trail',
		placeholder: 'A new frame, and the trail it opens…'
	}
].map((v) => ({ ...v, value: v.value as GrowVerb, send: 'Grow', model: GROW_MODEL }));

/** The verbs on offer, ask first. */
export const aiVerbs = (grow: boolean): VerbOption[] => (grow ? [ASK, ...GROW] : [ASK]);

export const isGrow = (verb: AiVerb): verb is GrowVerb => verb !== 'ask';
