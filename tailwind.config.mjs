/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
		extend: {
			colors: {
				brand: {
					bg: '#050505',
					surface: '#121212',
					accent: '#FF2D55',
					blue: '#007AFF',
					success: '#34C759',
				},
			},
			fontFamily: {
				sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
			},
			aspectRatio: {
				reel: '9 / 16',
			},
			animation: {
				'float': 'float 6s ease-in-out infinite',
				'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
			},
			keyframes: {
				float: {
					'0%, 100%': { transform: 'translateY(0)' },
					'50%': { transform: 'translateY(-10px)' },
				},
			},
			boxShadow: {
				'glow': '0 0 20px rgba(255, 45, 85, 0.3)',
			},
		},
	},
	plugins: [require('@tailwindcss/typography')],
};

