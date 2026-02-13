package com.viralprompt.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    private final com.viralprompt.service.CustomOAuth2UserService customOAuth2UserService;

    public SecurityConfig(com.viralprompt.service.CustomOAuth2UserService customOAuth2UserService) {
        this.customOAuth2UserService = customOAuth2UserService;
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(authorize -> authorize
                // Static resources and public pages
                .requestMatchers("/", "/ai-music", "/ai-books", "/ai-video-generator", "/caption-generator","/embed-content","/content/**").permitAll()
                .requestMatchers("/explore", "/prompt-library", "/reel-creator", "/script-writer", "/trending").permitAll()
                .requestMatchers("/prompt-detail", "/top-rated", "/signin", "/signup", "/error**", "/webjars/**").permitAll()
                .requestMatchers("/css/**", "/js/**", "/img/**", "/assets/**").permitAll()
                
                // Protected actions and user sections
                .requestMatchers("/submit", "/dashboard", "/profile", "/collections", "/analytics", "/settings").authenticated()
                
                // Protected mutation API endpoints (Rating, Commenting, Posting content)
                .requestMatchers(org.springframework.http.HttpMethod.POST, "/api/**").authenticated()
                .requestMatchers(org.springframework.http.HttpMethod.PUT, "/api/**").authenticated()
                .requestMatchers(org.springframework.http.HttpMethod.DELETE, "/api/**").authenticated()
                
                // Fallback for any other API or page not explicitly mentioned
                .anyRequest().authenticated()
            )
            .oauth2Login(oauth2 -> oauth2
                .loginPage("/login")
                .userInfoEndpoint(userInfo -> userInfo
                    .userService(customOAuth2UserService)
                )
                .defaultSuccessUrl("/dashboard", true)
            )
            .logout(logout -> logout
                .logoutSuccessUrl("/")
                .permitAll()
            );

        return http.build();
    }
}
