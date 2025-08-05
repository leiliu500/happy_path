const createExpoWebpackConfigAsync = require('@expo/webpack-config');

module.exports = async function(env, argv) {
  const config = await createExpoWebpackConfigAsync({
    ...env,
    babel: {
      dangerouslyAddModulePathsToTranspile: [
        // Add packages that need to be transpiled
        '@expo',
        'expo',
        'react-native',
        'react-native-web',
        'react-navigation',
        '@react-navigation',
        'react-native-vector-icons',
        'react-native-gesture-handler',
        'react-native-reanimated',
        'react-native-safe-area-context',
        'react-native-screens',
        'expo-haptics',
        'expo-linear-gradient',
        'expo-status-bar',
      ]
    }
  }, argv);

  // Customize config
  config.resolve.alias = {
    ...config.resolve.alias,
    'react-native$': 'react-native-web',
    'react-native-linear-gradient': 'expo-linear-gradient',
  };

  // Add support for CSS files
  config.module.rules.push({
    test: /\.css$/,
    use: ['style-loader', 'css-loader'],
  });

  return config;
};
