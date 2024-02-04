#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <SDL2/SDL_image.h>
#include <stdio.h>
#include "log.h"

int W = 1800;
int H = 1000;
int PW = 4;

SDL_Window* window = NULL;
SDL_Renderer* renderer = NULL;
TTF_Font* font = NULL;


int main(int argc, char* argv[]) {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
        return 1;
    }

    if (TTF_Init() == -1) {
        printf("SDL_ttf could not initialize! SDL_ttf Error: %s\n", TTF_GetError());
        return 1;
    }
    window = SDL_CreateWindow("SDL Window", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, W, H, SDL_WINDOW_SHOWN | SDL_WINDOW_RESIZABLE);
    if (window == NULL) {
        printf("Window could not be created! SDL_Error: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (renderer == NULL) {
        printf("Renderer could not be created! SDL Error: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    font = TTF_OpenFont("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16); // Ensure the Helvetica font file is available
    if (font == NULL) {
        printf("Failed to load font! SDL_ttf Error: %s\n", TTF_GetError());
        SDL_DestroyRenderer(renderer);
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    initLog();
    logText("- Applying a Rule to a Qube always results in defining a Qube of one higher dimension.");
    logText("- The user can draw a Qube of 2 dimensions (or 1 dimension if your height is 1, since thats just a line) and use that as a seed");
    logText("- We will call a group of cells a Qube (how cute)");
    logText("    otherwise it will be a 0.");
    logText("    if any given cell is in a state that is in your Rule, it will be a 1 on the next layer");
    logText("- A Rule can be thought of as a collection of states a given cell and its neighbors can be in");
    logText("- In this application you can chart your user defined Rules of N dimensions");
    logText("_,.+*\"*+.,_,.+*\"*+ Wxlys Petri Dish +*\"*+.,_,.+*\"*+.,_");
    
    SDL_Event event;
    int SHOULD_RUN = 1;
    while (SHOULD_RUN) {
      SDL_RenderClear(renderer);
      SDL_SetRenderDrawColor(renderer, 100, 100, 100, 255);
      renderLog();
      SDL_RenderPresent(renderer);
      while (SDL_PollEvent(&event)) {
	if (event.type == SDL_QUIT) {
	  SHOULD_RUN = 0;
	} else if (event.type == SDL_KEYDOWN) {
	  switch (event.key.keysym.sym) {
	  case SDLK_ESCAPE:
	    SHOULD_RUN = 0;
	    break;
	  case SDLK_SPACE:
	    toggleLog(1);
	  }
	} else if (event.type == SDL_KEYUP) {
	  switch (event.key.keysym.sym) {
	  case SDLK_SPACE:
	    toggleLog(0);
	  }
	} else if (event.type == SDL_WINDOWEVENT) {
	  switch (event.window.event) {
	  case SDL_WINDOWEVENT_SIZE_CHANGED:
	    // Update the renderer's viewport or any other necessary adjustments due to window size change.
	    W = event.window.data1; // New width
	    H = event.window.data2; // New height
	    SDL_RenderSetViewport(renderer, &(SDL_Rect){0, 0, W, H});
	    break;
	  }
        }
      }
    }
    // Cleanup
    teardownLog();
    TTF_CloseFont(font);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    TTF_Quit();
    SDL_Quit();
    
    return 0;
}

