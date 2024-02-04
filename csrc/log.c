#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include "log.h"

SDL_Texture* logTexture;
int show_log = 0;
TTF_Font* font;
extern int W;
extern int H;
int WIDTH, HEIGHT;
extern SDL_Window* window;
extern SDL_Renderer* renderer;
TTF_Font* logFont;

SDL_Texture* previous_render_target;

void initLog() {
  WIDTH = W;
  HEIGHT = H;
  logTexture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, WIDTH, HEIGHT);
  logFont = TTF_OpenFont("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16); 
  clearLog();
}

void clearLog() {
  previous_render_target = SDL_GetRenderTarget(renderer);
  SDL_SetRenderTarget(renderer, logTexture);
  SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
  SDL_RenderClear(renderer);
  SDL_SetRenderTarget(renderer, previous_render_target);
}

void logText(const char* text) {
  if (text == NULL) return;
  printf("%s\n", text);
  previous_render_target = SDL_GetRenderTarget(renderer);
  // Create a surface for the new text
  SDL_Color textColor = {0, 0, 0, 0};
  SDL_Surface* textSurface = TTF_RenderText_Solid(logFont, text, textColor);
  SDL_Texture* textTexture = SDL_CreateTextureFromSurface(renderer, textSurface);
  
  // Create a new texture as target for updated log
  SDL_Texture* newLogTexture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, WIDTH, HEIGHT);
  
  // Set the new texture as the render target
  SDL_SetRenderTarget(renderer, newLogTexture);
  SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
  SDL_RenderClear(renderer);
  
  // Copy the old log texture into the new one, shifted down
  SDL_Rect dstrect = {0, 16, WIDTH, HEIGHT - 16};
  SDL_RenderCopy(renderer, logTexture, NULL, &dstrect);
  
  // Copy the new text into the new log texture
  SDL_Rect textRect = {0, 0, textSurface->w, textSurface->h};
  SDL_RenderCopy(renderer, textTexture, NULL, &textRect);
  
  // Replace the old log texture with the new one
  SDL_DestroyTexture(logTexture);
  logTexture = newLogTexture;
  
  // Reset render target to the default
  SDL_SetRenderTarget(renderer, NULL);
  
  // Cleanup
  SDL_FreeSurface(textSurface);
  SDL_DestroyTexture(textTexture);
  SDL_SetRenderTarget(renderer, previous_render_target);
}

void renderLog() {
  SDL_Rect dest;
  SDL_Rect source;
  if (!show_log) {
    source.x = 0;
    source.y = 0;
    source.w = WIDTH;
    source.h = 64;
    dest.x = 0;
    dest.y = 0;
    dest.w = WIDTH;
    dest.h = 64;
  } else {
    source.x = 0;
    source.y = 0;
    source.w = WIDTH;
    source.h = HEIGHT;
    dest.x = 0;
    dest.y = 0;
    dest.w = WIDTH;
    dest.h = HEIGHT;
  }
  
  SDL_RenderCopy(renderer, logTexture, &source, &dest);
}

void teardownLog() {
  SDL_DestroyTexture(logTexture);
  TTF_CloseFont(logFont);
}

void toggleLog(int toggle) {
  show_log = toggle;
}
