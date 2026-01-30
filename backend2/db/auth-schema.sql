CREATE SCHEMA auth;

-- 2. Create the users table
CREATE TABLE auth.users (
                            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                            email TEXT UNIQUE NOT NULL,
                            encrypted_password TEXT NOT NULL,
                            created_at TIMESTAMPTZ DEFAULT now()
);