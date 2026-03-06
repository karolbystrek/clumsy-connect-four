from easyAI import AI_Player, Negamax, SSS
from clumsy_connect_four import ConnectFour

def main():
    ai_algo_neg = Negamax(5)
    ai_algo_sss = SSS(5)
    
    # Initialize the Clumsy Connect Four game with 50% slip probability
    game = ConnectFour([AI_Player(ai_algo_neg), AI_Player(ai_algo_sss)], slip_probability=0.5)
    
    game.play()
    
    if game.lose():
        print("Player %d wins." % (game.opponent_index))
    else:
        print("Looks like we have a draw.")

if __name__ == "__main__":
    main()
