const USERS_KEY = 'whms_users';
const TOKEN_KEY = 'authToken';
const USER_KEY = 'authUser';

const DEFAULT_USERS = [
  {
    id: 'dev-owner',
    name: 'Victor Wahome',
    email: 'owner@whms.com',
    password: 'owner123',
    role: 'owner',
    avatar: '/images/avatars/owner.jpg',
  },
  {
    id: 'dev-admin',
    name: 'Alice Wahome',
    email: 'admin@whms.com',
    password: 'admin123',
    role: 'admin',
    avatar: '/images/avatars/admin.jpg',
  },
  {
    id: 'dev-manager',
    name: 'Peter Mwangi',
    email: 'manager@whms.com',
    password: 'manager123',
    role: 'manager',
    avatar: '/images/avatars/manager.jpg',
  },
  {
    id: 'dev-worker',
    name: 'John Kamau',
    email: 'worker@whms.com',
    password: 'worker123',
    role: 'worker',
    avatar: '/images/avatars/worker.jpg',
  },
];

function getUsers() {
  const storedUsers = localStorage.getItem(USERS_KEY);

  if (!storedUsers) {
    localStorage.setItem(USERS_KEY, JSON.stringify(DEFAULT_USERS));
    return DEFAULT_USERS;
  }

  return JSON.parse(storedUsers);
}

function saveUsers(users) {
  localStorage.setItem(USERS_KEY, JSON.stringify(users));
}

function createToken(user) {
  return `mock-token-${user.id}-${Date.now()}`;
}

export const authService = {
  login: async (email, password) => {
    const users = getUsers();

    const user = users.find(
      (item) =>
        item.email.toLowerCase() === email.toLowerCase() &&
        item.password === password
    );

    if (!user) {
      throw new Error('Invalid email or password.');
    }

    const { password: _, ...safeUser } = user;

    const token = createToken(safeUser);

    return {
      token,
      user: safeUser,
    };
  },

  signup: async (payload) => {
    const users = getUsers();

    const existingUser = users.find(
      (user) =>
        user.email.toLowerCase() === payload.email.toLowerCase()
    );

    if (existingUser) {
      throw new Error('An account with this email already exists.');
    }

    const newUser = {
      id: `user-${Date.now()}`,
      name: payload.name,
      email: payload.email,
      password: payload.password,

      // New public accounts are workers by default.
      // Admin/Owner accounts should not be created through public signup.
      role: 'worker',

      avatar: '/images/avatars/default.jpg',
    };

    users.push(newUser);
    saveUsers(users);

    const { password: _, ...safeUser } = newUser;

    const token = createToken(safeUser);

    return {
      token,
      user: safeUser,
    };
  },

  getCurrentUser: async () => {
    const token = localStorage.getItem(TOKEN_KEY);
    const storedUser = localStorage.getItem(USER_KEY);

    if (!token || !storedUser) {
      throw new Error('No active session.');
    }

    return {
      data: JSON.parse(storedUser),
    };
  },

  logout: async () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  },
};

export default authService;