export const PATHS = {
  login: '/login',
  signup: '/signup',
  dashboard: '/',
  animals: '/animals',
  animalDetail: (id = ':id') => `/animals/${id}`,
  breeding: '/breeding',
  feed: '/feed',
  vaccinations: '/vaccinations',
  alerts: '/alerts',
  notifications: '/notifications',
  sales: '/sales',
  reports: '/reports',
  users: '/users',
  settings: '/settings',
  profile: '/profile',
  dailyOperations: '/daily-operations',
};

export default PATHS;