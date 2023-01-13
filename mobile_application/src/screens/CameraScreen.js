import React, { useState, useEffect } from 'react';
import { Text, View, StyleSheet } from 'react-native';
import { BarCodeScanner } from 'expo-barcode-scanner';
import AsyncStorage from '@react-native-async-storage/async-storage';
import jwt_decode from "jwt-decode";
import { Crypt, RSA } from 'hybrid-crypto-js';
import base64 from "react-native-base64";

const CameraScreen = ({ navigation, params }) => {
  const [hasPermission, setHasPermission] = useState(null);
  const [scanned, setScanned] = useState(false);

  useEffect(() => {
    const getBarCodeScannerPermissions = async () => {
      const { status } = await BarCodeScanner.requestPermissionsAsync();
      setHasPermission(status === 'granted');
    };

    getBarCodeScannerPermissions();
  }, []);

  const signRSA = async (message) => {
    var rsa = new RSA();
    var crypt = new Crypt();
    const publicKey = await AsyncStorage.getItem('@publicKey')
    const privateKey = await AsyncStorage.getItem('@privateKey')

    if ((publicKey !== null) && (privateKey !== null)) {
      const signature = JSON.parse(crypt.signature(privateKey, message));
      return signature.signature;
    } else {
      return
    }
  }

  const createJWT = async (action, token, name) => {
    const mobileAppID = await AsyncStorage.getItem('@mobileAppID')
    var header = base64.encode(JSON.stringify({ alg: "RS256", type: "JWT", kid: mobileAppID }));
    var newHeader = header.replace(/=/g, '');
    var payload = base64.encode(JSON.stringify({ action: action, token: token, name: name }));
    var newPayload = payload.replace(/=/g, '')
    var signature = await signRSA(`${newHeader}.${newPayload}`);

    var JWT = `${header}.${payload}.${signature}`;
    var newJWT = JWT.replace(/=/g, '')
    return newJWT
  }
  const sendJWT = async (action, JWT) => {
    const addressIP = await AsyncStorage.getItem('@serverIP')
    fetch(`http://${addressIP}/v1/${action}/get/authorize`, {
      method: 'GET',
      headers: { "Authorization": JWT },
    })
      .then((response) => response)
      .then((responseJson) => {
      })
      .catch((error) => {
        console.error(error);
      })
  };
  const handleBarCodeScanned = async ({ data }) => {
    setScanned(true);
    const addressIP = await AsyncStorage.getItem('@serverIP')
    const publicKey = await AsyncStorage.getItem('@publicKey')
    const privateKey = await AsyncStorage.getItem('@privateKey')
    const mobileAppID = await AsyncStorage.getItem('@mobileAppID')
    if (addressIP !== null && publicKey !== null && privateKey !== null && mobileAppID !== null) {
      try {
        const token = jwt_decode(data);
        await AsyncStorage.setItem('@oldQR', data)
        if (token.action === 'login') {
          var tempName = await AsyncStorage.getItem(`${token.name}`)
          if (tempName !== null) {
            var JWT = await createJWT(token.action, token.token, token.name);
            sendJWT("login", JWT)
            alert(`Authorized ${token.name}`)
            navigation.navigate("Index", { QR: `${data}` })
          } else {
            alert("Not able to login")
          }
        } else if (token.action === 'register') {
          var tempName = await AsyncStorage.getItem(`${token.name}`)
          if (tempName === null) {
            var JWT = await createJWT(token.action, token.token, token.name);
            sendJWT("register", JWT)
            await AsyncStorage.setItem(`${token.name}`, token.name)
            alert(`Registered ${token.name}`)
            navigation.navigate("Index", { QR: `${data}` })
          } else {
            alert("Not able to register")
          }
        } else {
          alert("Malformed token")
        }
      } catch {
        alert("Unrecognized token")
      }
    } else {
      alert("Connect to server")
    }
    navigation.navigate("Index")
  };

  if (hasPermission === null) {
    return <Text>Requesting for camera permission</Text>;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  return (
    <View style={styles.container}>
      <BarCodeScanner
        onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
        style={styles.container}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'center',
  },
});

export default CameraScreen;

