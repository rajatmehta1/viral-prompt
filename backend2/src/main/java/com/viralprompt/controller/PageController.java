package com.viralprompt.controller;

import com.viralprompt.dto.EmbedContentDTO;
import com.viralprompt.model.Category;
import com.viralprompt.model.ContentItem;
import com.viralprompt.model.EmbedPromptStep;
import com.viralprompt.repository.CategoryRepository;
import com.viralprompt.service.ContentService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.List;
import java.util.Optional;

@Controller
public class PageController {

    private ContentService contentService;
    private CategoryRepository categoryRepository;

    @Autowired
    public PageController(ContentService contentService, CategoryRepository categoryRepository) {
        this.contentService = contentService;
        this.categoryRepository = categoryRepository;
    }

    @GetMapping("/")
    public String index(Model model) {
        model.addAttribute("trendingItems", contentService.getTrendingContent());
        return "index";
    }

    @GetMapping("/signin")
    public String signin() {
        return "signin";
    }

    @GetMapping("/signup")
    public String signup() {
        return "signup";
    }

    @GetMapping("/ai-music")
    public String aiMusic() {
        return "ai-music";
    }

    @GetMapping("/ai-books")
    public String aiBooks() {
        return "ai-books";
    }

    @GetMapping("/ai-video-generator")
    public String aiVideo() {
        return "ai-video-generator";
    }

    @GetMapping("/caption-generator")
    public String captionGenerator() {
        return "caption-generator";
    }

    @GetMapping("/dashboard")
    public String dashboard() {
        return "dashboard";
    }

    @GetMapping("/explore")
    public String explore() {
        return "explore";
    }

    @GetMapping("/profile")
    public String profile() {
        return "profile";
    }

    @GetMapping("/collections")
    public String collections() {
        return "collections";
    }

    @GetMapping("/analytics")
    public String analytics() {
        return "analytics";
    }

    @GetMapping("/prompt-library")
    public String promptLibrary() {
        return "prompt-library";
    }

    @GetMapping("/reel-creator")
    public String reelCreator() {
        return "reel-creator";
    }

    @GetMapping("/script-writer")
    public String scriptWriter() {
        return "script-writer";
    }

    @GetMapping("/settings")
    public String settings() {
        return "settings";
    }

    @GetMapping("/trending")
    public String trending() {
        return "trending";
    }

    @GetMapping("/prompt-detail")
    public String promptDetail() {
        return "prompt-detail";
    }

    @GetMapping("/submit")
    public String submit() {
        return "submit";
    }

    @GetMapping("/top-rated")
    public String topRated() {
        return "top-rated";
    }

    @GetMapping("/embed-content")
    public String embedContent(Model model) {
        model.addAttribute("embedContent", new EmbedContentDTO());
        model.addAttribute("categories", categoryRepository.findAll());
        return "embed-content";
    }

    @PostMapping("/embed-content")
    public String saveEmbedContent(@ModelAttribute EmbedContentDTO embedContent, 
                                   RedirectAttributes redirectAttributes) {
        try {
            ContentItem saved = contentService.saveEmbeddedContent(embedContent);
            redirectAttributes.addFlashAttribute("successMessage", "Content shared successfully!");
            return "redirect:/content/" + saved.getId();
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("errorMessage", "Error saving content: " + e.getMessage());
            return "redirect:/embed-content";
        }
    }

    @GetMapping("/content/{id}")
    public String viewContent(@PathVariable Long id, Model model) {
        Optional<ContentItem> contentItem = contentService.getContentById(id);
        if (contentItem.isPresent()) {
            model.addAttribute("content", contentItem.get());
            List<EmbedPromptStep> promptSteps = contentService.getPromptStepsForContent(id);
            model.addAttribute("promptSteps", promptSteps);
            return "content-detail";
        }
        return "redirect:/";
    }
}

