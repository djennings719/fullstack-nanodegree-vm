select players.id, players.name, count(matches.winner)
from players
left join matches on matches.winner = players.id
group by players.id;



select player1.id, player1.name, player2.id, player2.name
from players player1
join (
  select id, name, count(matches.winner) countPlayer2
  from players
  left join matches on matches.winner = players.id
  group by players.id
) as player2
on player2.countPlayer2 = (select count(matches.winner) from matches where matches.winner = player1.id)
where player1.id < player2.id
group by player1.id, player2.id, player2.name

;




