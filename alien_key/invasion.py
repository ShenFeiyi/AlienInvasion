from game import Game

def run_game():
    
    game = Game()    
    while True:
        game.check_events()
        if game.game_active:
            game.update_sprites()
        game.update_screen()

if __name__ == '__main__':
    run_game()
