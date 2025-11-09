import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { leaderboardApi } from '@/services/api';
import { Trophy, TrendingUp, Target } from 'lucide-react';

type LeaderboardType = 'weekly' | 'all-time' | 'accuracy';

export default function Leaderboard() {
  const [activeTab, setActiveTab] = useState<LeaderboardType>('weekly');

  const { data: weeklyData } = useQuery({
    queryKey: ['leaderboard-weekly'],
    queryFn: async () => {
      const response = await leaderboardApi.getWeeklyLeaderboard();
      return response.data;
    },
    enabled: activeTab === 'weekly',
  });

  const { data: allTimeData } = useQuery({
    queryKey: ['leaderboard-all-time'],
    queryFn: async () => {
      const response = await leaderboardApi.getAllTimeLeaderboard();
      return response.data;
    },
    enabled: activeTab === 'all-time',
  });

  const { data: accuracyData } = useQuery({
    queryKey: ['leaderboard-accuracy'],
    queryFn: async () => {
      const response = await leaderboardApi.getAccuracyLeaderboard();
      return response.data;
    },
    enabled: activeTab === 'accuracy',
  });

  const currentData =
    activeTab === 'weekly'
      ? weeklyData
      : activeTab === 'all-time'
      ? allTimeData
      : accuracyData;

  const tabs = [
    { id: 'weekly' as LeaderboardType, label: 'Weekly Profit', icon: TrendingUp },
    { id: 'all-time' as LeaderboardType, label: 'All-Time Profit', icon: Trophy },
    { id: 'accuracy' as LeaderboardType, label: 'Prediction Accuracy', icon: Target },
  ];

  const getRankColor = (rank: number) => {
    if (rank === 1) return 'text-yellow-500';
    if (rank === 2) return 'text-gray-400';
    if (rank === 3) return 'text-orange-600';
    return 'text-gray-500';
  };

  const getRankBadge = (rank: number) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return rank;
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Leaderboard</h1>
        <p className="text-gray-400">See how you rank against other traders</p>
      </div>

      {/* Tabs */}
      <div className="card">
        <div className="flex space-x-2 border-b border-dark-700">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-3 border-b-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-500'
                    : 'border-transparent text-gray-400 hover:text-white'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Leaderboard Table */}
        <div className="mt-6">
          {currentData && currentData.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-dark-700">
                    <th className="text-left py-3 px-4 text-gray-400 font-medium w-20">Rank</th>
                    <th className="text-left py-3 px-4 text-gray-400 font-medium">Username</th>
                    <th className="text-right py-3 px-4 text-gray-400 font-medium">
                      {activeTab === 'weekly'
                        ? 'Weekly Profit'
                        : activeTab === 'all-time'
                        ? 'All-Time Profit'
                        : 'Accuracy'}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {currentData.map((entry: any) => (
                    <tr
                      key={entry.user_id}
                      className={`border-b border-dark-700 ${
                        entry.rank <= 3 ? 'bg-dark-700/50' : ''
                      }`}
                    >
                      <td className="py-4 px-4">
                        <span className={`text-2xl font-bold ${getRankColor(entry.rank)}`}>
                          {getRankBadge(entry.rank)}
                        </span>
                      </td>
                      <td className="py-4 px-4">
                        <span className="text-white font-medium">{entry.username}</span>
                      </td>
                      <td className="text-right py-4 px-4">
                        <span className="text-white font-bold text-lg">
                          {activeTab === 'accuracy'
                            ? `${entry.prediction_accuracy?.toFixed(1)}%`
                            : activeTab === 'weekly'
                            ? `${entry.weekly_profit?.toFixed(2)} WC`
                            : `${entry.all_time_profit?.toFixed(2)} WC`}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-12">
              <Trophy className="w-16 h-16 text-gray-600 mx-auto mb-4" />
              <p className="text-gray-400">No leaderboard data available yet</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
