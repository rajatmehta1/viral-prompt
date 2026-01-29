# ViralPrompt Database

PostgreSQL database schema for the ViralPrompt platform.

## Files

| File | Description |
|------|-------------|
| `schema.sql` | Complete database schema with all tables, indexes, and triggers |
| `seed.sql` | Sample data for development and testing |

## Schema Overview

### Core Tables

- **users** - User accounts and profiles
- **user_followers** - Follower relationships
- **user_settings** - User preferences

### Prompts

- **prompts** - AI prompts library
- **prompt_categories** - Prompt categories (Image, Video, Music, etc.)
- **prompt_tags** - Tags for categorizing prompts
- **prompt_tag_relations** - Many-to-many prompt-tag relationships
- **prompt_likes** / **prompt_saves** - User interactions

### Content

- **content** - Generated images, videos, music, AI art
- **content_tags** - Content tagging
- **content_likes** / **content_views** - Engagement tracking
- **comments** - User comments (supports threading)

### Collections

- **collections** - User-created collections
- **collection_items** - Items in collections (content or prompts)

### AI Generation

- **generation_jobs** - AI generation job queue
- **credit_transactions** - Credit usage tracking

### Analytics

- **trending_content** - Trending leaderboard
- **trending_hashtags** - Popular hashtags
- **user_analytics** - Daily user stats
- **notifications** - User notifications

## Setup

### 1. Create Database

```bash
createdb viralprompt
```

### 2. Run Schema

```bash
psql -d viralprompt -f schema.sql
```

### 3. Load Seed Data (Development Only)

```bash
psql -d viralprompt -f seed.sql
```

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/viralprompt
```

## Entity Relationship Diagram

```
users ─────┬──────── prompts ─────── prompt_categories
           │              │
           │              └──── prompt_tags
           │
           ├──────── content ─────── content_views
           │              │
           │              └──── comments
           │
           ├──────── collections ─── collection_items
           │
           ├──────── generation_jobs
           │
           └──────── credit_transactions
```

## Key Features

- **UUID primary keys** for all main entities
- **JSONB fields** for flexible settings storage
- **Automatic timestamps** via triggers
- **Cascading deletes** for data integrity
- **Optimized indexes** for common queries
- **Credit system** for AI generation tracking
