import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
    type: 'content',
    // Type-check frontmatter using a schema
    schema: z.object({
        title: z.string(),
        description: z.string(),
        // Transform string to Date object
        pubDate: z.coerce.date(),
        updatedDate: z.coerce.date().optional(),
        heroImage: z.string().optional(),
        tags: z.array(z.string()).optional(),
        tier: z.string().optional(),
        category: z.enum(['News', 'Knowledge', 'Review']),
    }),
});

const coupons = defineCollection({
    type: 'data',
    schema: z.object({
        id: z.string(),
        firm_name: z.string(),
        category: z.string(),
        discount_highlight: z.string(),
        title: z.string().optional(),
        description: z.string().optional(),
        coupon_code: z.string(),
        expiration_date: z.string().optional(),
        theme_color: z.string(),
        features: z.array(z.string()),
        affiliate_link: z.string(),
        seo_content: z.string(),
        youtube_metadata: z.object({
            title: z.string(),
            description: z.string()
        }).optional(),
        trust_score: z.string().optional(),
        reviews_count: z.string().optional(),
        leverage: z.string().optional(),
        leverage_details: z.any().optional(),
        commissions: z.any().optional(),
        challenges: z.array(z.any()).optional(),
        consistency_rules: z.any().optional(),
        forbidden_strategies: z.array(z.string()).optional(),
        platforms: z.array(z.string()).optional(),
        instruments: z.array(z.string()).optional(),
        payment_methods: z.array(z.string()).optional(),
        payout_methods: z.array(z.string()).optional(),
        founded: z.string().optional(),
        payout_policy: z.any().optional(),
        firm_rules: z.any().optional(),
        timeline: z.array(z.any()).optional(),
        broker: z.string().optional(),
        video_source: z.object({
            type: z.string(),
            src: z.string().optional(),
            id: z.string().optional()
        }).optional(),
        firm_logo: z.string(),
        created_at: z.string()
    }),
});

const reviews = defineCollection({
    type: 'content',
    schema: z.object({
        title: z.string(),
        description: z.string(),
        pubDate: z.coerce.date(),
        updatedDate: z.coerce.date().optional(),
        heroImage: z.string().optional(),
        tags: z.array(z.string()).optional(),
        tier: z.string().optional(),
        category: z.string().optional(), // Flexible for reviews
    }),
});

export const collections = { blog, coupons, reviews };
