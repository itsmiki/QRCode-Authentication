import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, TextInput, TouchableOpacity } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import base64 from "react-native-base64";
import { Crypt, RSA } from 'hybrid-crypto-js';

const ServerScreen = () => {
    const [addressIP, setIP] = useState();

    const signRSA = async () => {
        var rsa = new RSA();
        var crypt = new Crypt();
        const publicKey = await AsyncStorage.getItem('@publicKey')
        // console.log(publicKey)
        const privateKey = await AsyncStorage.getItem('@privateKey')
        // console.log(privateKey)

        if ((publicKey !== null) && (privateKey !== null)) {

        } else {
            rsa.generateKeyPair(function (keyPair) {
                var publicKey = keyPair.publicKey;
                try {
                    AsyncStorage.setItem('@publicKey', publicKey)
                } catch (e) {
                    console.log(e)
                }
                var privateKey = keyPair.privateKey;
                try {
                    AsyncStorage.setItem('@privateKey', privateKey)
                } catch (e) {
                    console.log(e)
                }
            }, 1024);
        }
    }

    const removeKeys = async () => {
        try {
            await AsyncStorage.removeItem('@publicKey')
        } catch (e) {
            alert(e);
        }
        try {
            await AsyncStorage.removeItem('@privateKey')
        } catch (e) {
            alert(e);
        }
        try {
            await AsyncStorage.removeItem('@mobileAppID')
        } catch (e) {
            alert(e);
        }
    }

    const saveIP = async (value) => {

        try {
            await AsyncStorage.setItem('@serverIP', addressIP)
        } catch (e) {

        }
    }
    const loadIP = async () => {
        try {
            const addressIP = await AsyncStorage.getItem('@serverIP')
            if (addressIP !== null) {
                setIP(addressIP);
            }
        } catch (e) {
            alert(e)
        }
    }
    const removeIP = async () => {
        try {
            await AsyncStorage.removeItem('@serverIP')
        } catch (e) {
            alert(e);
        } finally {
            setIP("");
        }
    }

    useEffect(() => {
        loadIP()
    }, []);

    const getData = () => {
        fetch(`http://${addressIP}/v1/connect/get/mobile-id`, {
            method: 'GET',
        })
            .then((response) => response.json())
            .then((responseJson) => {
                console.log(responseJson);
                AsyncStorage.setItem('@mobileAppID', responseJson)
            })
            .catch((error) => {
                console.error(error);
            })
    };

    const sendData = async () => {
        const publicKey = await AsyncStorage.getItem('@publicKey')
        console.log(`Publickey = ${publicKey}`)
        const mobileAppID = await AsyncStorage.getItem('@mobileAppID')
        console.log(`MobileAppID = ${mobileAppID}`)
        fetch(`http://${addressIP}/v1/connect/get/mobile-app/${mobileAppID}/key/${base64.encode(publicKey)}`, {
            method: 'GET',
        })
            .then((response) => response)
            .then((responseJson) => {
            })
            .catch((error) => {
                console.error(error);
            })
    };

    const connect = async () => {
        const oldIP = await AsyncStorage.getItem('@serverIP')
        if (oldIP === addressIP) {
            alert("IP already used")
        } else {
            alert("Connecting")
            saveIP();
            await signRSA();
            getData();

            setTimeout(() => {
                sendData();
            }, 500);
            alert("Connected")
        }
    }

    return (
        <View style={styles.container} >
            <Text style={styles.ip}>Server IP</Text>
            <Text style={styles.ip}>{addressIP}</Text>
            <Text></Text>

            <TextInput style={styles.input} onChangeText={(text) => setIP(text)} value={addressIP} />

            <TouchableOpacity style={styles.button} onPress={() => connect()}>
                <Text style={{ color: "white" }}>Connect</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.button} onPress={() => removeIP()}>
                <Text style={{ color: "white" }} >Delete IP</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.button} onPress={() => removeKeys()}>
                <Text style={{ color: "white" }} >Delete Keys</Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#fff",
        alignItems: "center",
    },
    ip: {
        fontSize: 24,
        fontWeight: "300",
        color: "black",
    },
    input: {
        borderWidth: 1,
        borderColor: "#575DD9",
        alignSelf: 'stretch',
        margin: 32,
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
        marginTop: 32,
        marginHorizontal: 32,
        borderRadius: 6,
    }
});

export default ServerScreen;