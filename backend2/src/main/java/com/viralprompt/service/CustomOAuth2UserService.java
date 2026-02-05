package com.viralprompt.service;

import com.viralprompt.model.Profile;
import com.viralprompt.repository.ProfileRepository;
import org.springframework.security.oauth2.client.userinfo.DefaultOAuth2UserService;
import org.springframework.security.oauth2.client.userinfo.OAuth2UserRequest;
import org.springframework.security.oauth2.core.OAuth2AuthenticationException;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Map;
import java.util.Optional;
import java.util.UUID;

@Service
public class CustomOAuth2UserService extends DefaultOAuth2UserService {

    private final ProfileRepository profileRepository;

    public CustomOAuth2UserService(ProfileRepository profileRepository) {
        this.profileRepository = profileRepository;
    }

    @Override
    @Transactional
    public OAuth2User loadUser(OAuth2UserRequest userRequest) throws OAuth2AuthenticationException {
        OAuth2User oauth2User = super.loadUser(userRequest);
        
        String registrationId = userRequest.getClientRegistration().getRegistrationId();
        Map<String, Object> attributes = oauth2User.getAttributes();
        
        String email = null;
        String name = null;
        String picture = null;
        
        if ("google".equalsIgnoreCase(registrationId)) {
            email = (String) attributes.get("email");
            name = (String) attributes.get("name");
            picture = (String) attributes.get("picture");
        } else if ("facebook".equalsIgnoreCase(registrationId)) {
            email = (String) attributes.get("email");
            name = (String) attributes.get("name");
            Map<String, Object> pictureObj = (Map<String, Object>) attributes.get("picture");
            if (pictureObj != null) {
                Map<String, Object> data = (Map<String, Object>) pictureObj.get("data");
                if (data != null) {
                    picture = (String) data.get("url");
                }
            }
        } else if ("twitter".equalsIgnoreCase(registrationId)) {
            // Twitter API v2 user-info attribute mapping
            Map<String, Object> data = (Map<String, Object>) attributes.get("data");
            if (data != null) {
                name = (String) data.get("name");
                picture = (String) data.get("profile_image_url");
                // Twitter OAuth2 might not always provide email unless requested/permitted
            }
        }
        
        if (email != null) {
            updateOrCreateProfile(email, name, picture);
        }
        
        return oauth2User;
    }

    private void updateOrCreateProfile(String email, String name, String avatarUrl) {
        Optional<Profile> profileOpt = profileRepository.findByEmail(email);
        
        if (profileOpt.isPresent()) {
            Profile profile = profileOpt.get();
            profile.setDisplayName(name);
            profile.setAvatarUrl(avatarUrl);
            profileRepository.save(profile);
        } else {
            Profile profile = Profile.builder()
                    .id(UUID.randomUUID()) // In a real Supabase setup, this would link to auth.users
                    .email(email)
                    .username(email.split("@")[0] + "_" + UUID.randomUUID().toString().substring(0, 5))
                    .displayName(name)
                    .avatarUrl(avatarUrl)
                    .build();
            profileRepository.save(profile);
        }
    }
}
