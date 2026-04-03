// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
	site: 'https://gopropreels.com',
	integrations: [
		tailwind(),
		sitemap({
			changefreq: 'daily',
			priority: 0.7,
			filter: (page) =>
				!page.includes('/go/') &&
				!page.includes('/debug') &&
				!page.includes('/poster-demo') &&
				!page.includes('/api/'),
			serialize(item) {
				if (item.url === 'https://gopropreels.com/') {
					item.priority = 1.0;
					item.changefreq = 'daily';
				} else if (item.url.match(/\/(forex|futures|crypto)\/$/)) {
					item.priority = 0.9;
					item.changefreq = 'daily';
				} else if (item.url.match(/\/(forex|futures|crypto)\/[^/]+/)) {
					item.priority = 0.8;
					item.changefreq = 'weekly';
				} else if (item.url.includes('/coupons/')) {
					item.priority = 0.8;
					item.changefreq = 'weekly';
				} else if (item.url.includes('/blog/') || item.url.includes('/news/')) {
					item.priority = 0.6;
					item.changefreq = 'weekly';
				} else if (item.url.includes('/compare/')) {
					item.priority = 0.7;
					item.changefreq = 'weekly';
				} else if (item.url.includes('/privacy') || item.url.includes('/terms')) {
					item.priority = 0.3;
					item.changefreq = 'monthly';
				}
				return item;
			},
		}),
	],
	server: {
		headers: {
			"Access-Control-Allow-Origin": "*"
		}
	}
});
