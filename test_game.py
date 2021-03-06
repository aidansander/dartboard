from game import Player, Game
from game import CountDownPlayer
from dart import Dart

def setup_test_game_2p():
    p1 = Player("Player1")
    p2 = Player("Player2")
    g = Game([p1, p2])

    return g


def test_game_0():

    g = setup_test_game_2p()

    g.record_dart(Dart(3, 20))
    g.record_dart(Dart(1, 6))
    g.record_dart(Dart(3, 20))
    g.record_dart(Dart(2, 17))


    assert g.players[0].hist[0] == Dart(3,20) 
    assert g.players[0].hist[1] == Dart(1,6) 
    assert g.players[0].hist[2] == Dart(3,20) 

    assert g.players[1].hist[0] == Dart(2,17) 


def test_game_undo_dart():
    g = setup_test_game_2p()

    g.record_dart(Dart(3, 20))
    g.record_dart(Dart(1, 6))
    g.record_dart(Dart(3, 20))
    g.undo_dart()
    g.record_dart(Dart(2, 17))


    assert g.players[0].hist[0] == Dart(3,20) 
    assert g.players[0].hist[1] == Dart(1,6) 
    assert g.players[0].hist[2] == Dart(2,17) 
    assert g.players[1].hist == []
    
def test_CountDownPlayer_double_in():
    p = CountDownPlayer("Player1", 301, True, False)
    p.record_dart(Dart(1, 20))
    p.record_dart(Dart(2, 20))
    p.record_dart(Dart(2, 20))
    assert p.roundscore == 301-80
    
    p = CountDownPlayer("Player1", 301, True, False)
    p.record_dart(Dart(1, 20))
    p.record_dart(Dart(1, 20))
    p.record_dart(Dart(3, 20))
    assert p.roundscore == 301
