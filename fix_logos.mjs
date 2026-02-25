import fs from 'fs';
import path from 'path';

const logosDir = 'd:/Dropbox/@Code _offical/New_skills/website_GoPropReels.com_new/public/images/logos';
const couponsDir = 'd:/Dropbox/@Code _offical/New_skills/website_GoPropReels.com_new/src/content/coupons';

// 1. Get all actual logo files
const actualFiles = fs.readdirSync(logosDir);

// Helper to find the best match for a given basename
function findActualFile(referencedPath) {
    if (!referencedPath) return null;
    const basename = path.basename(referencedPath, path.extname(referencedPath));
    // Try to find a file with the same basename but different extension
    const match = actualFiles.find(f => {
        const actualBasename = path.basename(f, path.extname(f));
        return actualBasename.toLowerCase() === basename.toLowerCase();
    });
    return match ? `/images/logos/${match}` : null;
}

// 2. Process each JSON file
const jsonFiles = fs.readdirSync(couponsDir).filter(f => f.endsWith('.json'));

let fixedCount = 0;

jsonFiles.forEach(file => {
    const filePath = path.join(couponsDir, file);
    const content = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    let modified = false;

    // Check firm_logo
    if (content.firm_logo) {
        const actualLogo = findActualFile(content.firm_logo);
        if (actualLogo && actualLogo !== content.firm_logo) {
            console.log(`Fixing firm_logo for ${file}: ${content.firm_logo} -> ${actualLogo}`);
            content.firm_logo = actualLogo;
            modified = true;
        }
    }

    // Check video_source.src
    if (content.video_source && content.video_source.type === 'image' && content.video_source.src) {
        const actualVideoSrc = findActualFile(content.video_source.src);
        if (actualVideoSrc && actualVideoSrc !== content.video_source.src) {
            console.log(`Fixing video_source for ${file}: ${content.video_source.src} -> ${actualVideoSrc}`);
            content.video_source.src = actualVideoSrc;
            modified = true;
        }
    }

    if (modified) {
        fs.writeFileSync(filePath, JSON.stringify(content, null, 2));
        fixedCount++;
    }
});

console.log(`Finished. Fixed ${fixedCount} files.`);
