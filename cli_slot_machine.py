import random
import time
import os

class CLISlotMachine:
    def __init__(self):
        self.fruits = ["🍒", "🍋", "🍊", "🍉", "💎"]
        self.fruit_names = ["Cherry", "Lemon", "Orange", "Watermelon", "Diamond"]
        self.reels = [0, 0, 0, 0, 0]
        self.balance = 100
        self.bet = 10
        self.total_winnings = 0
    
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def display_header(self):
        print("\n" + "="*60)
        print("                    🎰 SLOT MACHINE 🎰")
        print("="*60)
        print(f"Balance: ${self.balance} | Bet: ${self.bet} | Total Winnings: ${self.total_winnings}")
        print("="*60 + "\n")
    
    def display_reels(self):
        print("┌─────────────────────────────────────────┐")
        print("│", end="")
        for fruit in self.reels:
            print(f"  {self.fruits[fruit]}  ", end="")
        print("  │")
        print("└─────────────────────────────────────────┘")
        print()
    
    def spin_animation(self):
        print("SPINNING...\n")
        
        spins_per_reel = 15
        for spin in range(spins_per_reel):
            print("\r", end="")
            print("┌─────────────────────────────────────────┐")
            print("│", end="")
            for i in range(5):
                self.reels[i] = random.randint(0, 4)
                print(f"  {self.fruits[self.reels[i]]}  ", end="")
            print("  │")
            print("└─────────────────────────────────────────┘", end="")
            time.sleep(0.1)
        
        print("\n")
    
    def check_win(self):
        first_reel = self.reels[0]
        
        # Check for 5 of a kind
        if all(reel == first_reel for reel in self.reels):
            winnings = self.bet * 50
            self.balance += winnings
            self.total_winnings += winnings
            print("🎉 " + "="*50 + " 🎉")
            print(f"    JACKPOT!!! 5x {self.fruit_names[first_reel]}")
            print(f"    YOU WON: ${winnings}")
            print("🎉 " + "="*50 + " 🎉\n")
            return
        
        # Check for 4 of a kind
        if self.reels.count(first_reel) == 4:
            winnings = self.bet * 20
            self.balance += winnings
            self.total_winnings += winnings
            print("🎊 " + "="*50 + " 🎊")
            print(f"    GREAT! 4x {self.fruit_names[first_reel]}")
            print(f"    YOU WON: ${winnings}")
            print("🎊 " + "="*50 + " 🎊\n")
            return
        
        # Check for 3 of a kind
        for fruit in range(5):
            if self.reels.count(fruit) == 3:
                winnings = self.bet * 10
                self.balance += winnings
                self.total_winnings += winnings
                print("😊 " + "="*50 + " 😊")
                print(f"    NICE! 3x {self.fruit_names[fruit]}")
                print(f"    YOU WON: ${winnings}")
                print("😊 " + "="*50 + " 😊\n")
                return
        
        # Check for 3 in a row (consecutive)
        for i in range(3):
            if self.reels[i] == self.reels[i+1] == self.reels[i+2]:
                winnings = self.bet * 5
                self.balance += winnings
                self.total_winnings += winnings
                print("👍 " + "="*50 + " 👍")
                print("    CONSECUTIVE! 3 in a row")
                print(f"    YOU WON: ${winnings}")
                print("👍 " + "="*50 + " 👍\n")
                return
        
        # No win
        print("❌ " + "="*50 + " ❌")
        print("    NO MATCH - TRY AGAIN!")
        print("❌ " + "="*50 + " ❌\n")
    
    def spin(self):
        if self.balance < self.bet:
            print(f"❌ Insufficient balance! You need ${self.bet} but only have ${self.balance}\n")
            return False
        
        self.balance -= self.bet
        self.spin_animation()
        self.display_reels()
        self.check_win()
        return True
    
    def change_bet(self):
        print("\nCurrent bet: $" + str(self.bet))
        try:
            new_bet = int(input("Enter new bet amount: $"))
            if new_bet <= 0:
                print("❌ Bet must be greater than 0!\n")
                return
            if new_bet > self.balance:
                print(f"❌ Bet cannot exceed your balance (${self.balance})!\n")
                return
            self.bet = new_bet
            print(f"✓ Bet changed to ${self.bet}\n")
        except ValueError:
            print("❌ Invalid input! Please enter a number.\n")
    
    def show_menu(self):
        print("\nOptions:")
        print("  1. SPIN (Press Enter or type '1')")
        print("  2. Change Bet (Type '2')")
        print("  3. View Fruits (Type '3')")
        print("  4. Quit (Type '4')")
        print()
    
    def show_fruits(self):
        print("\nFruit Values:")
        print("="*40)
        for i, (emoji, name) in enumerate(zip(self.fruits, self.fruit_names)):
            print(f"  {emoji}  {name}")
        print("="*40)
        print("\nWin Conditions:")
        print("  5 of a kind  = 50x bet")
        print("  4 of a kind  = 20x bet")
        print("  3 of a kind  = 10x bet")
        print("  3 in a row   = 5x bet")
        print()
    
    def run(self):
        while True:
            self.clear_screen()
            self.display_header()
            
            if self.balance == 0:
                print("😢 You're out of money! Game Over!")
                print(f"Total Winnings: ${self.total_winnings}")
                print()
                return
            
            self.display_reels()
            self.show_menu()
            
            choice = input("Your choice: ").strip().lower()
            
            if choice == "1" or choice == "":
                self.spin()
            elif choice == "2":
                self.change_bet()
            elif choice == "3":
                self.show_fruits()
                input("Press Enter to continue...")
            elif choice == "4":
                self.clear_screen()
                print("\n" + "="*60)
                print("Thanks for playing! Final Stats:")
                print(f"  Final Balance: ${self.balance}")
                print(f"  Total Winnings: ${self.total_winnings}")
                print("="*60 + "\n")
                break
            else:
                print("❌ Invalid choice! Please try again.")
                time.sleep(1)

if __name__ == "__main__":
    game = CLISlotMachine()
    game.run()
