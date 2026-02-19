/**
 * SEO Helper Functions
 * Auto-generate SEO-friendly alt text and internal links
 */

interface Deal {
	id: string;
	firm_name: string;
	category: string;
	discount_highlight: string;
	coupon_code: string;
	features?: string[];
}

/**
 * Auto-generate SEO-friendly alt text for deal images
 */
export function generateImageAltText(deal: Deal, context: 'card' | 'landing' = 'card'): string {
	const { firm_name, discount_highlight, coupon_code, category } = deal;

	const categoryMap: Record<string, string> = {
		forex: 'forex prop firm',
		futures: 'futures prop firm',
		crypto: 'crypto prop firm',
		stock: 'stock prop firm',
	};

	const categoryLabel = categoryMap[category] || `${category} prop firm`;

	if (context === 'landing') {
		return `${firm_name} ${discount_highlight} discount coupon code ${coupon_code} - ${categoryLabel} trading account deal`;
	}

	return `${firm_name} ${discount_highlight} coupon code - ${categoryLabel} prop firm deal`;
}

/**
 * Get related deals for internal linking
 */
export function getRelatedDeals(
	currentDeal: Deal,
	allDeals: Deal[],
	options: {
		sameCategory?: boolean;
		sameFirm?: boolean;
		maxResults?: number;
	} = {}
): Deal[] {
	const {
		sameCategory = true,
		sameFirm = false,
		maxResults = 3,
	} = options;

	let related = allDeals.filter((deal) => deal.id !== currentDeal.id);

	if (sameCategory) {
		related = related.filter((deal) => deal.category === currentDeal.category);
	}

	if (sameFirm) {
		related = related.filter((deal) => deal.firm_name === currentDeal.firm_name);
	}

	// Shuffle for variety
	related = related.sort(() => Math.random() - 0.5);

	return related.slice(0, maxResults);
}

/**
 * Get deals by category for category pages
 */
export function getDealsByCategory(allDeals: Deal[], category: string): Deal[] {
	if (category === 'all') return allDeals;
	return allDeals.filter((deal) => deal.category === category);
}

/**
 * Generate breadcrumbs for landing page
 */
export function generateBreadcrumbs(deal: Deal): Array<{ label: string; url: string }> {
	return [
		{ label: 'Home', url: '/' },
		{ label: 'Deals', url: '/#feed' },
		{ label: deal.category.charAt(0).toUpperCase() + deal.category.slice(1), url: `/?category=${deal.category}` },
		{ label: deal.firm_name, url: `/?q=${encodeURIComponent(deal.firm_name)}` },
	];
}

