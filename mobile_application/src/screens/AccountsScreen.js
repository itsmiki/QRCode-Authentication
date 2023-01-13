import React, { useState, useEffect } from "react";
import { StyleSheet, View, Text, FlatList, TouchableOpacity, TextInput } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Crypt, RSA } from 'hybrid-crypto-js';
import base64 from "react-native-base64";

const AccountsScreen = ({navigation}) => {

    const [accounts, setAccounts] = useState([]);
    const [webName, deleteWebName] = useState();

    const removeWeb = async (webName) => {
        try {
            await AsyncStorage.removeItem(`${webName}`)
        } catch (e) {
            alert(e);
        }
        const JWT = await createJWT("delete", webName)
        sendJWT("delete", JWT)
        navigation.navigate("Index")
    }

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

    const createJWT = async (action, name) => {
        const mobileAppID = await AsyncStorage.getItem('@mobileAppID')
        var header = base64.encode(JSON.stringify({ alg: "RS256", type: "JWT", kid: mobileAppID }));
        var newHeader = header.replace(/=/g, '');
        var payload = base64.encode(JSON.stringify({ action: action, name: name }));
        var newPayload = payload.replace(/=/g, '')
        var signature = await signRSA(`${newHeader}.${newPayload}`);

        var JWT = `${header}.${payload}.${signature}`;
        var newJWT = JWT.replace(/=/g, '')
        return newJWT
    }
    const sendJWT = async (action, JWT) => {
        const addressIP = await AsyncStorage.getItem('@serverIP')
        fetch(`http://${addressIP}/v1/${action}/get/account`, {
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

    useEffect(() => {
        const fetchData = async () => {
            setAccounts(await AsyncStorage.getAllKeys())
        }
        fetchData();
    }, []);

    function removeA(arr) {
        var what, a = arguments, L = a.length, ax;
        while (L > 1 && arr.length) {
            what = a[--L];
            while ((ax = arr.indexOf(what)) !== -1) {
                arr.splice(ax, 1);
            }
        }
        return arr;
    }

    removeA(accounts, '@oldQR');
    removeA(accounts, '@privateKey');
    removeA(accounts, '@publicKey');
    removeA(accounts, '@serverIP');
    removeA(accounts, '@mobileAppID');

    return (
        <View>
            <Text style={styles.title} >Your accounts</Text>
            <FlatList
                data={accounts}
                renderItem={(item) => (
                    <Text style={styles.text}>{item.item}</Text>
                )}
            />
            <Text style={styles.title} >Delete account</Text>
            <TextInput style={styles.input} onChangeText={(text) => deleteWebName(text)} value={webName} />
            <TouchableOpacity style={styles.button} onPress={() => removeWeb(webName)}>
                <Text style={{ color: "white" }} >Delete Web</Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    title: {
        fontSize: 40,
        fontWeight: "500",
        color: "black",
        alignSelf: "center",
        marginTop: 20,
    },
    text: {
        fontSize: 24,
        fontWeight: "300",
        borderWidth: 1,
        borderColor: "#575DD9",
        alignSelf: 'stretch',
        marginLeft: 15,
        marginRight: 15,
        marginTop: 10,
        borderRadius: 6,
        paddingHorizontal: 16,
        padding: 10,
    },
    input: {
        borderWidth: 1,
        borderColor: "#575DD9",
        alignSelf: 'stretch',
        margin: 32,
        marginTop: 15,
        height: 64,
        borderRadius: 6,
        paddingHorizontal: 16,
        fontSize: 24,
        fontWeight: "300"
    },
    button: {
        backgroundColor: "#575DD9",
        alignItems: "center",
        justifyContent: "center",
        alignSelf: "stretch",
        paddingVertical: 12,
        paddingHorizontal: 32,
        marginBottom: 24,
        marginHorizontal: 32,
        borderRadius: 6,
    }
})

export default AccountsScreen;