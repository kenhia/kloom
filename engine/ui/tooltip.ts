import type { Action } from 'svelte/action';
import { placeTip, TIP_GRACE, tipWait } from '../tooltip';

/**
 * The HUD's tooltip (docs/design.md §Tooltips, korg 3540): `use:tooltip={text}`
 * on an icon-only control in place of a `title`. It shows on hover and on
 * keyboard focus after a short wait (engine/tooltip.ts), stays while the
 * pointer is on it, and goes on Esc, blur, a press or the pointer leaving
 * (WCAG 1.4.13). It is hidden from assistive technology: the control's own
 * name already says it, and a `title` beside that name was heard twice.
 *
 * One tooltip element serves the page, coloured from the control's palette
 * when it is shown, so it matches the scene or the reading it sits in.
 */

let tip: HTMLDivElement | null = null;
let owner: HTMLElement | null = null;
/** A tooltip waiting to show, and whose; and one waiting to hide. */
let showTimer: ReturnType<typeof setTimeout> | undefined;
let pending: HTMLElement | null = null;
let hideTimer: ReturnType<typeof setTimeout> | undefined;
let hidAt: number | null = null;

function element(): HTMLDivElement {
	if (tip?.isConnected) return tip;
	tip = document.createElement('div');
	tip.className = 'kloom-tooltip';
	tip.setAttribute('aria-hidden', 'true');
	tip.hidden = true;
	Object.assign(tip.style, {
		position: 'fixed',
		zIndex: '1000',
		maxWidth: '18rem',
		padding: '0.25rem 0.5rem',
		borderRadius: '0.25rem',
		border: '1px solid',
		font: '0.8125rem/1.3 var(--sans, system-ui, sans-serif)',
		whiteSpace: 'normal',
		pointerEvents: 'auto',
		boxShadow: '0 2px 8px rgb(0 0 0 / 0.25)'
	});
	// Hoverable (WCAG 1.4.13): moving onto the tooltip keeps it.
	tip.addEventListener('pointerenter', () => clearTimeout(hideTimer));
	tip.addEventListener('pointerleave', () => hide(owner, TIP_GRACE));
	document.body.append(tip);
	return tip;
}

/** The control's palette, read off it: the shell and the scene set these. */
function colour(node: HTMLElement, el: HTMLDivElement) {
	const css = getComputedStyle(node);
	const read = (name: string, fallback: string) => css.getPropertyValue(name).trim() || fallback;
	el.style.color = read('--background', 'Canvas');
	el.style.background = read('--ink', 'CanvasText');
	el.style.borderColor = read('--background', 'Canvas');
}

function show(node: HTMLElement, text: string) {
	pending = null;
	clearTimeout(hideTimer);
	const el = element();
	owner = node;
	el.textContent = text;
	colour(node, el);
	el.hidden = false;
	const at = placeTip(
		node.getBoundingClientRect(),
		{ width: el.offsetWidth, height: el.offsetHeight },
		{ width: window.innerWidth, height: window.innerHeight }
	);
	el.style.left = `${at.left}px`;
	el.style.top = `${at.top}px`;
}

/** Hide the tooltip, if `node`'s is the one showing; after `wait` ms when given. */
function hide(node: HTMLElement | null, wait = 0) {
	if (node && pending === node) {
		clearTimeout(showTimer);
		pending = null;
	}
	if (!node || owner !== node) return;
	clearTimeout(hideTimer);
	const go = () => {
		if (owner !== node) return;
		if (tip && !tip.hidden) hidAt = Date.now();
		if (tip) tip.hidden = true;
		owner = null;
	};
	if (wait) hideTimer = setTimeout(go, wait);
	else go();
}

function escape(e: KeyboardEvent) {
	if (e.key !== 'Escape' || !tip || tip.hidden) return;
	// Dismissed, and that is all this Esc does: the page's own Esc stands down.
	e.preventDefault();
	hide(owner);
}

let listening = 0;

export const tooltip: Action<HTMLElement, string> = (node, initial) => {
	let text = initial;
	const showing = () => !!tip && !tip.hidden && owner !== null;
	const soon = () => {
		clearTimeout(showTimer);
		if (owner === node) {
			clearTimeout(hideTimer);
			return;
		}
		const wait = tipWait(Date.now(), hidAt, showing());
		if (wait) {
			pending = node;
			showTimer = setTimeout(() => show(node, text), wait);
		} else show(node, text);
	};
	const enter = (e: PointerEvent) => {
		if (e.pointerType !== 'touch') soon();
	};
	const leave = () => hide(node, TIP_GRACE);
	const focus = () => {
		if (node.matches(':focus-visible')) soon();
	};
	const blur = () => hide(node);
	const press = () => hide(node);
	const key = (e: KeyboardEvent) => {
		if (e.key === 'Enter' || e.key === ' ') hide(node);
	};

	node.addEventListener('pointerenter', enter);
	node.addEventListener('pointerleave', leave);
	node.addEventListener('focus', focus);
	node.addEventListener('blur', blur);
	node.addEventListener('pointerdown', press);
	node.addEventListener('keydown', key);
	if (listening++ === 0) window.addEventListener('keydown', escape, true);

	return {
		update(next) {
			text = next;
			if (owner === node && tip) tip.textContent = next;
		},
		destroy() {
			node.removeEventListener('pointerenter', enter);
			node.removeEventListener('pointerleave', leave);
			node.removeEventListener('focus', focus);
			node.removeEventListener('blur', blur);
			node.removeEventListener('pointerdown', press);
			node.removeEventListener('keydown', key);
			if (--listening === 0) window.removeEventListener('keydown', escape, true);
			hide(node);
		}
	};
};
