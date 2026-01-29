-- ViralPrompt Seed Data
-- Sample data for development and testing

-- ============================================
-- PROMPT CATEGORIES
-- ============================================

INSERT INTO prompt_categories (name, slug, description, icon, color, display_order) VALUES
('Image', 'image', 'Prompts for AI image generation (Midjourney, DALL-E, Stable Diffusion)', 'bi-image', '#4facfe', 1),
('Video', 'video', 'Prompts for AI video generation (Sora, Runway, Pika)', 'bi-camera-video', '#ec4899', 2),
('Music', 'music', 'Prompts for AI music generation (Suno, Udio)', 'bi-music-note-beamed', '#22c55e', 3),
('Caption', 'caption', 'Social media captions and hooks', 'bi-chat-quote', '#fbbf24', 4),
('Script', 'script', 'Video scripts and storytelling prompts', 'bi-file-earmark-text', '#a78bfa', 5),
('AI Art', 'ai-art', 'Artistic and creative AI prompts', 'bi-stars', '#f472b6', 6);

-- ============================================
-- PROMPT TAGS
-- ============================================

INSERT INTO prompt_tags (name, slug, use_count) VALUES
('portrait', 'portrait', 15200),
('cinematic', 'cinematic', 12400),
('landscape', 'landscape', 9800),
('fantasy', 'fantasy', 21300),
('aesthetic', 'aesthetic', 18700),
('viral', 'viral', 45800),
('lofi', 'lofi', 12400),
('trending', 'trending', 34500),
('hooks', 'hooks', 28900),
('nature', 'nature', 11200),
('cyberpunk', 'cyberpunk', 8900),
('anime', 'anime', 16700),
('realistic', 'realistic', 14300),
('abstract', 'abstract', 7600),
('documentary', 'documentary', 5400),
('product', 'product', 8700),
('commercial', 'commercial', 6500),
('motivation', 'motivation', 19800),
('chill', 'chill', 10200),
('dreamy', 'dreamy', 7800);

-- ============================================
-- SAMPLE USERS
-- ============================================

INSERT INTO users (id, email, username, password_hash, display_name, bio, avatar_url, is_verified, is_premium, credits_balance, role) VALUES
('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'alex@example.com', 'alexcreator', '$2b$10$example_hash_here', 'Alex Creator', 'Digital artist & AI enthusiast 🎨', 'https://i.pravatar.cc/100?img=33', TRUE, TRUE, 500, 'creator'),
('b2c3d4e5-f6a7-8901-bcde-f12345678901', 'sarah@example.com', 'ai_dreamweaver', '$2b$10$example_hash_here', 'Sarah Chen', 'Creating magical worlds with AI ✨', 'https://i.pravatar.cc/100?img=1', TRUE, TRUE, 350, 'creator'),
('c3d4e5f6-a7b8-9012-cdef-123456789012', 'jordan@example.com', 'lofi_beats', '$2b$10$example_hash_here', 'Jordan Lee', 'Lo-fi music producer | Chill vibes only 🎵', 'https://i.pravatar.cc/100?img=4', TRUE, FALSE, 120, 'creator'),
('d4e5f6a7-b8c9-0123-defa-234567890123', 'maya@example.com', 'naturelens', '$2b$10$example_hash_here', 'Maya Patel', 'Nature photographer exploring AI 🌿', 'https://i.pravatar.cc/100?img=3', TRUE, TRUE, 280, 'creator'),
('e5f6a7b8-c9d0-1234-efab-345678901234', 'demo@example.com', 'demouser', '$2b$10$example_hash_here', 'Demo User', 'Just exploring ViralPrompt!', 'https://i.pravatar.cc/100?img=10', FALSE, FALSE, 50, 'user');

-- ============================================
-- SAMPLE PROMPTS
-- ============================================

INSERT INTO prompts (id, user_id, category_id, title, prompt_text, description, type, preview_image_url, is_featured, use_count, like_count) VALUES
(
    'p1a2b3c4-d5e6-7890-abcd-111111111111',
    'b2c3d4e5-f6a7-8901-bcde-f12345678901',
    1,
    'Cinematic Portrait Master',
    'A cinematic portrait of [subject], shot on Kodak Portra 400, golden hour lighting, shallow depth of field, bokeh background, professional photography, 8K resolution, detailed skin texture, soft rim lighting',
    'Perfect for creating stunning portrait shots with that film-like quality',
    'image',
    'https://images.unsplash.com/photo-1686191128892-3b37add4b844?w=400',
    TRUE,
    15200,
    2100
),
(
    'p2b3c4d5-e6f7-8901-bcde-222222222222',
    'b2c3d4e5-f6a7-8901-bcde-f12345678901',
    2,
    'Dreamy Product Showcase',
    'Smooth cinematic camera movement around [product], floating in ethereal clouds, soft pastel lighting, dreamy atmosphere, 4K 60fps, professional commercial quality, subtle particle effects',
    'Create beautiful product videos that feel magical and premium',
    'video',
    'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400',
    TRUE,
    8700,
    1450
),
(
    'p3c4d5e6-f7a8-9012-cdef-333333333333',
    'c3d4e5f6-a7b8-9012-cdef-123456789012',
    3,
    'Lo-Fi Chill Beat Generator',
    'Create a lo-fi hip hop beat, 85 BPM, jazzy piano chords, vinyl crackle, mellow bass, soft drums, perfect for studying, rainy day vibes, nostalgic and warm mood, subtle tape wobble effect',
    'Generate relaxing lo-fi beats perfect for focus and studying',
    'music',
    NULL,
    TRUE,
    12400,
    3200
),
(
    'p4d5e6f7-a8b9-0123-defa-444444444444',
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
    1,
    'Epic Fantasy Landscape',
    'Breathtaking fantasy landscape, floating islands, bioluminescent plants, double sunset, ethereal mist, hyper-detailed, Greg Rutkowski and Thomas Kinkade style, 8K wallpaper, volumetric lighting, magical atmosphere',
    'Create stunning fantasy worlds with incredible detail',
    'image',
    'https://images.unsplash.com/photo-1682687220742-aba13b6e50ba?w=400',
    TRUE,
    21300,
    4500
),
(
    'p5e6f7a8-b9c0-1234-efab-555555555555',
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
    4,
    'Viral Hook Generator',
    'Generate 5 scroll-stopping hooks for [topic]. Each hook should: create curiosity using open loops, include at least one power word, be under 10 words, target [audience]. Tone: [conversational/professional/edgy]',
    'Create attention-grabbing hooks that stop the scroll',
    'caption',
    NULL,
    TRUE,
    45800,
    8900
),
(
    'p6f7a8b9-c0d1-2345-fabc-666666666666',
    'd4e5f6a7-b8c9-0123-defa-234567890123',
    2,
    'Nature Documentary Style',
    'Cinematic nature footage of [subject], BBC documentary style, macro lens details, slow motion 120fps, David Attenborough narration vibe, epic orchestral music mood, golden hour or blue hour lighting',
    'Create stunning nature content with documentary quality',
    'video',
    'https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=400',
    FALSE,
    6900,
    980
);

-- ============================================
-- SAMPLE CONTENT
-- ============================================

INSERT INTO content (id, user_id, prompt_id, title, description, type, media_url, thumbnail_url, is_ai_generated, ai_model, is_featured, view_count, like_count, share_count) VALUES
(
    'c1a2b3c4-d5e6-7890-abcd-aaaaaaaaaaaa',
    'b2c3d4e5-f6a7-8901-bcde-f12345678901',
    'p4d5e6f7-a8b9-0123-defa-444444444444',
    'Cyberpunk City Dreamscape',
    'A neon-lit cyberpunk cityscape generated with Midjourney v6',
    'ai_art',
    'https://images.unsplash.com/photo-1686191128892-3b37add4b844',
    'https://images.unsplash.com/photo-1686191128892-3b37add4b844?w=400',
    TRUE,
    'midjourney-v6',
    TRUE,
    2400000,
    89000,
    12500
),
(
    'c2b3c4d5-e6f7-8901-bcde-bbbbbbbbbbbb',
    'd4e5f6a7-b8c9-0123-defa-234567890123',
    NULL,
    'Mountain Sunrise Timelapse',
    'Beautiful sunrise over the Swiss Alps captured in 4K',
    'video',
    'https://example.com/videos/mountain-sunrise.mp4',
    'https://images.unsplash.com/photo-1682687220742-aba13b6e50ba?w=400',
    FALSE,
    NULL,
    TRUE,
    1800000,
    72000,
    9800
),
(
    'c3c4d5e6-f7a8-9012-cdef-cccccccccccc',
    'b2c3d4e5-f6a7-8901-bcde-f12345678901',
    NULL,
    'Abstract Flow Art',
    'Mesmerizing abstract fluid art animation',
    'ai_art',
    'https://images.unsplash.com/photo-1677442136019-21780ecad995',
    'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400',
    TRUE,
    'stable-diffusion-xl',
    TRUE,
    1200000,
    54000,
    6700
);

-- ============================================
-- SAMPLE COLLECTIONS
-- ============================================

INSERT INTO collections (id, user_id, name, description, cover_image_url, is_public, is_featured, item_count) VALUES
(
    'col1a2b3-c4d5-6789-abcd-111111111111',
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
    'Best of AI Art 2026',
    'Curated collection of the most stunning AI-generated artwork',
    'https://images.unsplash.com/photo-1686191128892-3b37add4b844?w=400',
    TRUE,
    TRUE,
    128
),
(
    'col2b3c4-d5e6-7890-bcde-222222222222',
    'd4e5f6a7-b8c9-0123-defa-234567890123',
    'Stunning Landscapes',
    'Breathtaking natural landscapes from around the world',
    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400',
    TRUE,
    TRUE,
    256
),
(
    'col3c4d5-e6f7-8901-cdef-333333333333',
    'b2c3d4e5-f6a7-8901-bcde-f12345678901',
    'Cinematic Moments',
    'Film-like stills and video clips with that cinematic feel',
    'https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=400',
    TRUE,
    FALSE,
    94
);

-- ============================================
-- TRENDING DATA
-- ============================================

INSERT INTO trending_content (content_id, rank_position, period, score) VALUES
('c1a2b3c4-d5e6-7890-abcd-aaaaaaaaaaaa', 1, 'daily', 98.5),
('c2b3c4d5-e6f7-8901-bcde-bbbbbbbbbbbb', 2, 'daily', 87.3),
('c3c4d5e6-f7a8-9012-cdef-cccccccccccc', 3, 'daily', 76.8);

INSERT INTO trending_hashtags (tag_id, rank_position, period, mention_count, is_hot) VALUES
(1, 1, 'daily', 45800, TRUE),
(2, 2, 'daily', 34500, TRUE),
(5, 3, 'daily', 28900, FALSE),
(8, 4, 'daily', 21300, TRUE),
(11, 5, 'daily', 18700, FALSE);
