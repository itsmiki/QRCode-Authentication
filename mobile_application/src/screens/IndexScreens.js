import React from "react";
import { View, Text, StyleSheet, TouchableOpacity, Image } from 'react-native';
import logo from './../../assets/logo.png'

const IndexScreen = ({navigation}) => {
    return (
        <View>
            <Image
                style={styles.logo}
                source={logo}
            />
            <Text style={styles.header}>turboAuthenticator</Text>
            <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Camera')}>
                <Text style={{color: "white"}}>Camera</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Accounts')}>
                <Text style={{color: "white"}}>Accounts</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Server')}>
                <Text style={{color: "white"}}>Server</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('About')}>
                <Text style={{color: "white"}}>About</Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    logo : {
        alignItems: "center",
        alignSelf: "center",
        margin: 20,
        width: 250,
        height: 250,
    },
    header: {
        fontSize: 24,
        fontWeight: "600",
        color: "black",
        alignSelf: 'center',
    }, 
    button : {
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

export default IndexScreen;