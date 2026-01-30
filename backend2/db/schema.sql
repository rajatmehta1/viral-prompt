-- ViralPrompt Supabase Schema

-- Profiles table (linked to Supabase Auth.users)
CREATE TABLE profiles (
    id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    display_name TEXT,
    avatar_url TEXT,
    bio TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Categories
CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    description TEXT,
    icon_class TEXT,
    cover_image_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Content Items
CREATE TYPE content_type AS ENUM ('IMAGE', 'VIDEO', 'REEL', 'AI');
CREATE TYPE platform_type AS ENUM ('TIKTOK', 'INSTAGRAM', 'YOUTUBE', 'OTHER');

CREATE TABLE content_items (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    media_url TEXT,
    thumbnail_url TEXT,
    author_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
    category_id BIGINT REFERENCES categories(id) ON DELETE SET NULL,
    type content_type DEFAULT 'IMAGE',
    platform platform_type DEFAULT 'OTHER',
    views_count BIGINT DEFAULT 0,
    likes_count BIGINT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Prompts
CREATE TABLE prompts (
    id BIGSERIAL PRIMARY KEY,
    content_item_id BIGINT REFERENCES content_items(id) ON DELETE CASCADE,
    prompt_text TEXT NOT NULL,
    author_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
    model_info TEXT,
    usage_count INTEGER DEFAULT 0,
    original_prompt_id BIGINT REFERENCES prompts(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Collections
CREATE TABLE collections (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    owner_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    is_public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Collection Items (Many-to-Many)
CREATE TABLE collection_items (
    id BIGSERIAL PRIMARY KEY,
    collection_id BIGINT REFERENCES collections(id) ON DELETE CASCADE,
    content_item_id BIGINT REFERENCES content_items(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(collection_id, content_item_id)
);

-- Interactions (Likes, Saves, etc.)
CREATE TYPE interaction_type AS ENUM ('LIKE', 'SAVE', 'SHARE');

CREATE TABLE interactions (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    content_item_id BIGINT REFERENCES content_items(id) ON DELETE CASCADE,
    type interaction_type NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS (Row Level Security) if using Supabase client directly, 
-- but since we use Spring Boot with Service Role / Connection String, we'll keep it simple for now.
-- However, adding basic indexes is good practice.
CREATE INDEX idx_content_items_category ON content_items(category_id);
CREATE INDEX idx_content_items_author ON content_items(author_id);
CREATE INDEX idx_prompts_author ON prompts(author_id);
CREATE INDEX idx_collections_owner ON collections(owner_id);
