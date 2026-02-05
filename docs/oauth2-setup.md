# Social Sign-On (OAuth2) Setup Guide

This document explains how to set up Google, Facebook, and Twitter (X) sign-on for the ViralPrompt backend.

## Overview

The application uses Spring Security OAuth2 Client to handle social logins. To make it work, you need to provide Client IDs and Client Secrets from each provider.

## Environment Variables

The `application.yml` is configured to use environment variables for sensitive information. You should set the following variables in your development environment or deployment platform (e.g., Render, Heroku):

| Provider | Client ID Variable | Client Secret Variable |
| :--- | :--- | :--- |
| **Google** | `GOOGLE_CLIENT_ID` | `GOOGLE_CLIENT_SECRET` |
| **Facebook** | `FACEBOOK_CLIENT_ID` | `FACEBOOK_CLIENT_SECRET` |
| **Twitter** | `TWITTER_CLIENT_ID` | `TWITTER_CLIENT_SECRET` |

---

## 1. Google Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to **APIs & Services > Credentials**.
4. Click **Create Credentials > OAuth client ID**.
5. Configure the Consent Screen if you haven't already.
6. Select **Web application** as the Application type.
7. Add Authorized Redirect URIs:
   - `http://localhost:8081/login/oauth2/code/google` (for local dev)
   - `https://your-domain.com/login/oauth2/code/google` (for production)
8. Copy the Client ID and Client Secret.

---

## 2. Facebook Setup

1. Go to the [Meta for Developers](https://developers.facebook.com/) portal.
2. Click **My Apps > Create App**.
3. Select an app type (e.g., "Consumer") and follow the prompts.
4. Add the **Facebook Login** product to your app.
5. In the Facebook Login settings, add Authorized Redirect URIs:
   - `http://localhost:8081/login/oauth2/code/facebook`
   - `https://your-domain.com/login/oauth2/code/facebook`
6. Go to **Settings > Basic** to find your App ID and App Secret.

---

## 3. Twitter (X) Setup

1. Go to the [Twitter Developer Portal](https://developer.twitter.com/).
2. Create a Project and an App.
3. In the App settings, enable **User authentication settings**.
4. Set App Type to **Web App, Native App**.
5. Enable **OAuth 2.0**.
6. Set the Callback URI / Redirect URL:
   - `http://localhost:8081/login/oauth2/code/twitter`
   - `https://your-domain.com/login/oauth2/code/twitter`
7. Copy the Client ID and Client Secret.

---

## Customization

### Redirect After Login

Currently, users are redirected to `/dashboard` after a successful login. You can change this in `com.viralprompt.config.SecurityConfig`.

### Saving User Data

If you want to save the user profile (name, email) to your database upon login, you can implement a custom `OAuth2UserService` and register it in the `SecurityConfig`.
