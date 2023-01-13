import { createAppContainer } from 'react-navigation';
import { createStackNavigator } from 'react-navigation-stack';
import IndexScreen from './src/screens/IndexScreens';
import CameraScreen from './src/screens/CameraScreen';
import ServerScreen from './src/screens/ServerScreen';
import AccountsScreen from './src/screens/AccountsScreen';
import AboutScreen from './src/screens/AboutScreen';

const navigator = createStackNavigator(
  {
    Index: IndexScreen,
    Camera: CameraScreen,
    Accounts: AccountsScreen,
    Server: ServerScreen,
    About: AboutScreen,
  },
  {
    initialRouteName: 'Index',
    defaultNavigationOptions: {
      title: 'turboAuthenticator',
    }
  }
);

export default createAppContainer(navigator);
