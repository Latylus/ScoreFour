
pointGenerators = [(x,y,z) for x in range(4) for y in range(4) for z in range(4) if x == 0 or y == 0 or z == 0]  
directions = [1,0,-1]
vectors = [(i,j,k) for i in directions for j in directions for k in directions if i!=0 or j!=0 or k!=0 ]
half_vectors = vectors[0:len(vectors)//2]
mirror_vectors = list(reversed(vectors[len(vectors)//2 :]))

class GameState:
    Grid = [[[None for k in range(4)] for j in range(4)] for i in range(4)]    
    IsPlayerZeroTurn = True
    LastMove = None
    MoveCount = 0

    def __init__(self) -> None:
        self.Grid = [[[None for k in range(4)] for j in range(4)] for i in range(4)]    
        self.IsPlayerZeroTurn = True
        self.MoveCount = 0

    def getPossibleMoves(self) -> list:
        return [(x,y) for x in range(4) for y in range(4) if None in self.Grid[x][y]] #None means a peg spot is empty


    def checkEnd(self) -> bool : 
        return self.getWinner() is not None or self.MoveCount == 64
    
    def getWinner(self) -> int:
        if self.LastMove is None :
            return None
        for vf, vb in zip(half_vectors, mirror_vectors):
            p0 = self.LastMove
            p1 = tuple(map(sum, zip(p0, vf)))
            p2 = tuple(map(sum, zip(p1, vf)))
            p3 = tuple(map(sum, zip(p2, vf))) 
            pm1 = tuple(map(sum, zip(p0, vb)))
            pm2 = tuple(map(sum, zip(pm1, vb)))
            pm3 = tuple(map(sum, zip(pm2, vb))) 
            inboundPoints = [p for p in [p0,p1,p2,p3,pm1,pm2,pm3] if all(c>=0 and c<4 for c in p)]
            lastMoveValue = self.Grid[p0[0]][p0[1]][p0[2]]
            if len(inboundPoints) >= 4 and all(V == lastMoveValue for V in [self.Grid[x][y][z] for (x,y,z) in inboundPoints]) :
                return lastMoveValue 
        return None

    def getWinnerWithNoPriorInfo(self) -> int:
        for (p,v) in [(point,vector) for point in pointGenerators for vector in vectors] :
            p0 = p
            p1 = tuple(map(sum, zip(p0, v)))
            p2 = tuple(map(sum, zip(p1, v)))
            p3 = tuple(map(sum, zip(p2, v)))
            points = [p0,p1,p2,p3]
            edgeValue = self.Grid[p0[0]][p0[1]][p0[2]]
            if edgeValue is not None and all(all(c>=0 and c<4 for c in p) for p in points) and all(edgeValue == V for V in [self.Grid[x][y][z] for (x,y,z) in points]) :
                return edgeValue 
        return None
    
    def playLegalMove(self, move : tuple) -> None:
        self.LastMove = (move[0],move[1],self.Grid[move[0]][move[1]].index(None))
        self.Grid[move[0]][move[1]][self.Grid[move[0]][move[1]].index(None) ] = 0 if self.IsPlayerZeroTurn else 1
        self.IsPlayerZeroTurn = not self.IsPlayerZeroTurn
        self.MoveCount += 1