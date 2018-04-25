__author__ = 'fj'


from pylab import *
from pandas import *
import sklearn
import statsmodels
from collections import defaultdict
from scipy.stats import norm




class TeamStats(object):
	def __init__(self, name):
		self.name = name
		self.pre_winp_by_year =  defaultdict( lambda : [0,0])
		self.reg_winp_by_year =  defaultdict( lambda : [0,0])

		self.pre_winp_by_team =  defaultdict( lambda : [0,0])
		self.reg_winp_by_team = defaultdict( lambda : [0,0])

		self.pre_winp =  [0,0]
		self.reg_winp =  [0,0]

		self.home_winp =  [0,0]
		self.away_winp =  [0,0]

	def update_stats(self, opponent, score, yr, month, home_game):
		win = 1 if score[0]>=score[1] else 0;

		if month <= 10:
			self.pre_winp_by_year[yr][0] += win
			self.pre_winp_by_year[yr][1] += 1
			self.pre_winp_by_team[opponent][0] += win
			self.pre_winp_by_team[opponent][1] += 1
			self.pre_winp[0]	 += win
			self.pre_winp[1]	 += 1
		else:
			self.reg_winp[0]	 += win
			self.reg_winp[1]	 += 1
			self.reg_winp_by_year[yr][0] +=  win
			self.reg_winp_by_year[yr][1] += 1
			self.reg_winp_by_team[opponent][0] += win
			self.reg_winp_by_team[opponent][1] += 1

		if home_game=='H':
			self.home_winp[0]	 += win
			self.home_winp[1]	 += 1
		elif home_game=='V':
			self.away_winp[0]	 += win
			self.away_winp[1]	 += 1


def get_bernouilli_pval(num_trials, win_count):
	"""
	approximate p-value of Bernouilli trials through Gaussian approxiamtion of binomial.
	:return:
	"""
	mv = num_trials*0.5;
	var = num_trials*0.25
	# compute the z-score
	z = (win_count - mv)/sqrt(var) # do we need a population correction factor ?
	if z > 0:
		p_val =	1-norm.cdf(z)
	else:
		p_val = norm.cdf(z)

	return p_val


# set up the data
data_fname = 'question_2_data/cumulative_statistics.csv'
data = DataFrame.from_csv(data_fname)



yearly_data = {};
team_stats = {}

# get team wise statistics
for rec in data.iterrows():
	yr = rec[0].year
	month = rec[0].month
	team =  rec[1]['TeamName']
	opponent =  rec[1]['Opponent']
	score = ( rec[1]['ScoreOff'], rec[1]['ScoreDef'] )
	home_game = rec[1]['homegame']
	try :
		team_stats[team]
	except KeyError:
		team_stats[team] = TeamStats(team)
	team_stats[team].update_stats( opponent, score, yr, month, home_game)

# look at home vs. away stats
home_games = 0
home_wins = 0
away_games = 0
away_wins = 0

for team in team_stats.keys():
	team_home_games = team_stats[team].home_winp[1]
	team_home_wins  = team_stats[team].home_winp[0]
	team_away_games = team_stats[team].away_winp[1]
	team_away_wins  = team_stats[team].away_winp[0]
	print '-------------------------------------------------------------------------------------------------------'
	print 'Statistics for team '+str(team)
	print '-------------------------------------------------------------------------------------------------------'
	print ' home games %d wins %d , win-pct %g' %(team_home_games, team_home_wins, team_home_wins/float(team_home_games)*100 )
	print ' away games %d wins %d , win-pct %g' %(team_away_games, team_away_wins, team_away_wins/float(team_away_games)*100 )
	# let's compute the p-value of this result under a null hypothesis of no bias (i.e fair chance)
	pval = get_bernouilli_pval( team_home_games, team_home_wins)
	print 'Under a fair odds null hypothesis approximate p-value is %g'%pval

	home_games += team_stats[team].home_winp[1]
	home_wins  += team_stats[team].home_winp[0]
	away_games += team_stats[team].away_winp[1]
	away_wins  += team_stats[team].away_winp[0]


# I'll divide by 2 because of the double counting of home vs away --- so 2 is approximately the inflation factor.
print '-------------------------------------------------------------------------------------------------------'
print 'CUMULATIVE STATISTICS'
print '-------------------------------------------------------------------------------------------------------'
print ' home games %d wins %d , win-pct %g' %(home_games/2, home_wins/2, home_wins/float(home_games)*100 )
print ' away games %d wins %d , win-pct %g' %(away_games/2, away_wins/2, away_wins/float(away_games)*100 )
pval = get_bernouilli_pval( home_games/2, home_wins/2)
print 'Under a fair odds null hypothesis approximate p-value is %g'%pval


# look at early vs. late stats
early_games = 0
early_wins = 0
late_games = 0
late_wins = 0

for team in team_stats.keys():
	team_early_games = team_stats[team].pre_winp[1]
	team_early_wins  = team_stats[team].pre_winp[0]
	team_late_games = team_stats[team].reg_winp[1]
	team_late_wins  = team_stats[team].reg_winp[0]
	print '-------------------------------------------------------------------------------------------------------'
	print 'Statistics for team '+str(team)
	print '-------------------------------------------------------------------------------------------------------'
	print ' early games %d wins %d , win-pct %g' %(team_early_games, team_early_wins, team_early_wins/float(team_early_games)*100 )
	print ' early games %d wins %d , win-pct %g' %(team_late_games, team_late_wins, team_late_wins/float(team_late_games)*100 )
	# let's compute the p-value of this result under a null hypothesis of no bias (i.e fair chance)
	pval = get_bernouilli_pval( team_early_games, team_early_wins)
	print 'Under a fair odds null hypothesis approximate p-value is %g'%pval

	# if team won more early than late games reverse the trend - just to accumulate properly
	if team_early_wins/float(team_early_games) >  team_late_wins/float(team_late_games):
		xx = team_early_games; team_early_games = team_late_games; team_late_games = xx;
		xx = team_early_wins; team_early_wins = team_late_wins; team_late_wins = xx;

	early_games +=team_early_games
	early_wins  += team_early_wins
	late_games += team_late_games
	late_wins  += team_late_wins


# I'll divide by 2 because of the double counting of home vs away --- so 2 is approximately the inflation factor.
print '-------------------------------------------------------------------------------------------------------'
print 'CUMULATIVE STATISTICS'
print '-------------------------------------------------------------------------------------------------------'
print ' good-half games %d wins %d , win-pct %g' %(early_games/2, early_wins/2, early_wins/float(early_games)*100 )
print ' poor-half games %d wins %d , win-pct %g' %(late_games/2, late_wins/2, late_wins/float(late_games)*100 )
pval = get_bernouilli_pval( early_games/2, early_wins/2)
print 'Under a fair odds null hypothesis approximate p-value is %g'%pval


# now let's look at early vs late season trends.

