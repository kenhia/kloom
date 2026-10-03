import type { Palette } from './model';

/**
 * Colour arithmetic for the brightness settings (docs/design.md §Brightness,
 * korg 3495): sRGB hex to and from OKLCH, and WCAG contrast. No dependency;
 * the matrices are Björn Ottosson's (https://bottosson.github.io/posts/oklab/).
 */

type Rgb = [number, number, number];

const toLinear = (c: number) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
const toGamma = (c: number) => (c <= 0.0031308 ? 12.92 * c : 1.055 * c ** (1 / 2.4) - 0.055);

/** `#rgb` or `#rrggbb` as linear-light sRGB channels, 0 to 1. */
function linear(hex: string): Rgb {
	let h = hex.replace('#', '');
	if (h.length === 3) h = [...h].map((c) => c + c).join('');
	return [0, 2, 4].map((i) => toLinear(parseInt(h.slice(i, i + 2), 16) / 255)) as Rgb;
}

function hex(rgb: Rgb): string {
	return (
		'#' +
		rgb
			.map((c) => {
				const v = Math.round(Math.min(1, Math.max(0, toGamma(Math.min(1, Math.max(0, c))))) * 255);
				return v.toString(16).padStart(2, '0');
			})
			.join('')
	);
}

/** OKLCH: lightness 0 to 1, chroma, hue in degrees. */
export interface Oklch {
	l: number;
	c: number;
	h: number;
}

export function toOklch(colour: string): Oklch {
	const [r, g, b] = linear(colour);
	const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
	const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
	const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
	const L = 0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s;
	const A = 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s;
	const B = 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s;
	return { l: L, c: Math.hypot(A, B), h: ((Math.atan2(B, A) * 180) / Math.PI + 360) % 360 };
}

/** Back to hex; a colour outside sRGB is clipped per channel. */
export function fromOklch({ l: L, c, h }: Oklch): string {
	const A = c * Math.cos((h * Math.PI) / 180);
	const B = c * Math.sin((h * Math.PI) / 180);
	const l = (L + 0.3963377774 * A + 0.2158037573 * B) ** 3;
	const m = (L - 0.1055613458 * A - 0.0638541728 * B) ** 3;
	const s = (L - 0.0894841775 * A - 1.291485548 * B) ** 3;
	return hex([
		4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
		-1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
		-0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s
	]);
}

/** WCAG 2 relative luminance. */
export function luminance(colour: string): number {
	const [r, g, b] = linear(colour);
	return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

/** WCAG 2 contrast ratio, 1 to 21. */
export function contrast(a: string, b: string): number {
	const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
	return (hi + 0.05) / (lo + 0.05);
}

/** The least contrast any text or line keeps against its background (WCAG AA body text). */
export const MIN_CONTRAST = 4.5;

/** How far one brightness step moves a background, in OKLCH lightness. */
export const BRIGHTNESS_STEP = 0.025;

/** The colours drawn on a palette's background, every one held to MIN_CONTRAST. */
const FOREGROUND = ['ink', 'muted', 'accent', 'line'] as const;

/**
 * A palette made brighter (positive steps) or dimmer (negative). Every
 * colour moves by the same lightness, so the palette keeps its look; then a
 * foreground that has fallen under MIN_CONTRAST is pushed away from the
 * background until it holds again. Zero steps is the palette itself.
 */
export function brighten(palette: Palette, steps: number): Palette {
	if (!steps) return palette;
	const shift = (colour: string) => {
		const o = toOklch(colour);
		return { ...o, l: Math.min(1, Math.max(0, o.l + steps * BRIGHTNESS_STEP)) };
	};
	const background = fromOklch(shift(palette.background));
	// Away from the background: darker on a light one, lighter on a dark one.
	const away = palette.scheme === 'light' ? -0.01 : 0.01;
	const out: Palette = { ...palette, background };
	for (const key of FOREGROUND) {
		const o = shift(palette[key]);
		let colour = fromOklch(o);
		while (contrast(colour, background) < MIN_CONTRAST && o.l > 0 && o.l < 1) {
			o.l = Math.min(1, Math.max(0, o.l + away));
			colour = fromOklch(o);
		}
		out[key] = colour;
	}
	return out;
}
