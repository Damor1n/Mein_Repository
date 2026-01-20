import chess
import os
import time
from typing import Tuple, Optional

class ChessBot:
    def __init__(self, depth=4):
        self.board = chess.Board()
        self.depth = depth
        self.nodes_evaluated = 0
        
        # Piece values for evaluation
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3.25,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0  # King value handled separately
        }
        
        # Piece-square tables for better evaluation
        self.pawn_table = [
            0,  0,  0,  0,  0,  0,  0,  0,
            5, 10, 10,-20,-20, 10, 10,  5,
            5, -5,-10,  0,  0,-10, -5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5,  5, 10, 25, 25, 10,  5,  5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0,  0,  0,  0,  0,  0,  0,  0
        ]
        
        self.knight_table = [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50
        ]
    
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def display_board(self):
        """Display the chess board in CLI format"""
        self.clear_screen()
        print("\n" + "="*50)
        print("           ♟ CHESS BOT 2000 ELO ♟")
        print("="*50 + "\n")
        
        board_str = self.board.__str__()
        lines = board_str.split('\n')
        
        print("  a b c d e f g h")
        for i, line in enumerate(lines):
            rank = 8 - i
            print(f"{rank} {line} {rank}")
        print("  a b c d e f g h\n")
        
        if self.board.is_checkmate():
            print("CHECKMATE!")
        elif self.board.is_check():
            print("⚠️  CHECK!")
        elif self.board.is_stalemate():
            print("STALEMATE!")
        
        print(f"Turn: {'White' if self.board.turn else 'Black'}")
        print()
    
    def evaluate_board(self) -> float:
        """Evaluate the board position"""
        if self.board.is_checkmate():
            return -10000 if self.board.turn else 10000
        
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0
        
        evaluation = 0
        
        # Material count
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                value = self.piece_values[piece.piece_type]
                
                # Apply piece-square tables
                if piece.piece_type == chess.PAWN:
                    idx = square if piece.color == chess.WHITE else 63 - square
                    value += self.pawn_table[idx] / 100
                elif piece.piece_type == chess.KNIGHT:
                    idx = square if piece.color == chess.WHITE else 63 - square
                    value += self.knight_table[idx] / 100
                
                # Add bonus for center control
                if piece.piece_type in [chess.KNIGHT, chess.BISHOP, chess.QUEEN]:
                    if square in [27, 28, 35, 36]:  # Center squares
                        value += 0.5
                
                if piece.color == chess.WHITE:
                    evaluation += value
                else:
                    evaluation -= value
        
        # Bonus for piece activity (number of legal moves)
        legal_moves = list(self.board.legal_moves)
        evaluation += len(legal_moves) * 0.05 * (1 if self.board.turn else -1)
        
        return evaluation
    
    def minimax(self, depth: int, alpha: float, beta: float, is_maximizing: bool) -> float:
        """Minimax algorithm with alpha-beta pruning"""
        self.nodes_evaluated += 1
        
        if depth == 0:
            return self.evaluate_board()
        
        if self.board.is_checkmate():
            return -10000 if self.board.turn else 10000
        
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0
        
        legal_moves = list(self.board.legal_moves)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                self.board.push(move)
                eval_score = self.minimax(depth - 1, alpha, beta, False)
                self.board.pop()
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                self.board.push(move)
                eval_score = self.minimax(depth - 1, alpha, beta, True)
                self.board.pop()
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    
    def get_best_move(self) -> Optional[chess.Move]:
        """Find the best move for current position"""
        legal_moves = list(self.board.legal_moves)
        
        if not legal_moves:
            return None
        
        best_move = legal_moves[0]
        best_value = float('-inf')
        
        self.nodes_evaluated = 0
        start_time = time.time()
        
        for move in legal_moves:
            self.board.push(move)
            value = self.minimax(self.depth - 1, float('-inf'), float('inf'), False)
            self.board.pop()
            
            if value > best_value:
                best_value = value
                best_move = move
        
        elapsed = time.time() - start_time
        print(f"🤖 Bot thinking... (evaluated {self.nodes_evaluated} positions in {elapsed:.2f}s)")
        
        return best_move
    
    def parse_move(self, move_str: str) -> Optional[chess.Move]:
        """Parse user move input (e.g., 'e2e4')"""
        try:
            move_str = move_str.strip().lower()
            if len(move_str) < 4:
                return None
            
            move = chess.Move.from_uci(move_str[:4])
            
            # Check for promotion
            if len(move_str) > 4:
                promotion_char = move_str[4]
                piece_map = {'q': chess.QUEEN, 'r': chess.ROOK, 'b': chess.BISHOP, 'n': chess.KNIGHT}
                if promotion_char in piece_map:
                    move = chess.Move(move.from_square, move.to_square, promotion=piece_map[promotion_char])
            
            if move in self.board.legal_moves:
                return move
            return None
        except:
            return None
    
    def play(self):
        """Main game loop"""
        print("\n" + "="*50)
        print("Welcome to Chess Bot 2000 ELO!")
        print("="*50)
        print("\nYou play as WHITE")
        print("Bot plays as BLACK")
        print("\nEnter moves in algebraic notation (e.g., 'e2e4')")
        print("Type 'quit' to exit\n")
        
        input("Press Enter to start...")
        
        while True:
            self.display_board()
            
            if self.board.is_checkmate():
                if self.board.turn:
                    print("🏆 You LOST! Black is checkmate!")
                else:
                    print("🎉 You WON! White is checkmate!")
                break
            
            if self.board.is_stalemate():
                print("🤝 DRAW by stalemate!")
                break
            
            if self.board.is_insufficient_material():
                print("🤝 DRAW by insufficient material!")
                break
            
            # Player's turn (White)
            if self.board.turn:
                while True:
                    move_input = input("Your move (or 'quit'): ").strip()
                    
                    if move_input.lower() == 'quit':
                        print("Thanks for playing!")
                        return
                    
                    move = self.parse_move(move_input)
                    if move:
                        self.board.push(move)
                        break
                    else:
                        print("❌ Invalid move! Try again (e.g., 'e2e4')")
            
            # Bot's turn (Black)
            else:
                bot_move = self.get_best_move()
                if bot_move:
                    self.board.push(bot_move)
                    print(f"Bot plays: {bot_move.uci()}\n")
                    time.sleep(0.5)
                else:
                    print("No legal moves available!")
                    break

if __name__ == "__main__":
    try:
        # Try to import chess library
        bot = ChessBot(depth=4)
        bot.play()
    except ImportError:
        print("Error: python-chess library is required.")
        print("Install it with: pip install python-chess")
