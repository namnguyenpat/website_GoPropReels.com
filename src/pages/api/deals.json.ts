import { getCollection } from 'astro:content';

export async function GET() {
    const coupons = await getCollection('coupons');
    const deals = coupons.map(c => c.data);

    return new Response(
        JSON.stringify(deals),
        {
            status: 200,
            headers: {
                "Content-Type": "application/json"
            }
        }
    );
}
