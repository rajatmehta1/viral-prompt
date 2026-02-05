package com.viralprompt.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class EmbedContentDTO {
    private String platform;
    private String embedUrl;
    private String title;
    private String category;
    private String description;
    private String tags;
    
    @Builder.Default
    private List<PromptStepDTO> promptSteps = new ArrayList<>();
}
