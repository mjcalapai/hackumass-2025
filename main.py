import pygame


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0




def place_piece(self, pos, piece, team):
    zone = self.zones.get(pos)
    if team == "white" and "white_territory" in zone:
        self.grid[pos] = piece
        piece.position = pos
        return True
    elif team == "black" and "black_territory" in zone:
        self.grid[pos] = piece
        piece.position = pos
        return True
    else:
        print("Invalid placement: outside your zone.")
        return False

while running:
   pass

pygame.quit()





















#testing board = Board()
# p = Slinger("white", (3,3))
# board.grid[(3,3)] = p
# print(p.valid_moves(board))
