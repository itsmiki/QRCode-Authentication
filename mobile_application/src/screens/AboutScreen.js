import React, { useState, useEffect } from "react";
import { StyleSheet, View, Text } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { ScrollView } from "react-native-gesture-handler";

const AccountsScreen = ({ navigation }) => {

    const [items, setItems] = useState(['1', '2', '3', '4']);

    useEffect(() => {
        const fetchData = async () => {
            const addressIP = await AsyncStorage.getItem('@serverIP')
            const mobileAppID = await AsyncStorage.getItem('@mobileAppID')
            const publicKey = await AsyncStorage.getItem('@publicKey')
            const privateKey = await AsyncStorage.getItem('@privateKey')

            setItems([addressIP, mobileAppID, publicKey, privateKey])
        }
        fetchData();

    }, []);

    return (
        <View>
            <ScrollView>
                <Text style={styles.text}>IP</Text>
                <Text style={{ paddingHorizontal: 16 }}>{items[0]}</Text>
                <Text style={styles.text}>mobileAppID</Text>
                <Text style={{ paddingHorizontal: 16 }}>{items[1]}</Text>
                <Text style={styles.text}>publicKey</Text>
                <Text style={{ paddingHorizontal: 16 }}>{items[2]}</Text>
                <Text style={styles.text}>privateKey</Text>
                <Text style={{ paddingHorizontal: 16 }}>{items[3]}</Text>
            </ScrollView>
        </View>
    );
};

const styles = StyleSheet.create({
    text: {
        fontSize: 20,
        fontWeight: "500",
        color: "black",
        alignSelf: 'stretch',
        marginTop: 10,
        paddingHorizontal: 16,
    }
})

export default AccountsScreen;