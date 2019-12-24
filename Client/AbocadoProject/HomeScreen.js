import React, { Component } from 'react';
import { StyleSheet, View, Text, Button, ScrollView, Dimensions } from 'react-native';
import VacationList from './Vacation/components/VacationList';
import VacationInfo from './Vacation/components/VacationInfo';
import VacationType from './Vacation/components/VacationType';

const { height } = Dimensions.get('window');
export default class HomeScreen extends Component {
  state = {
    screenHeight: height,
  };

  onContentSizeChange = (contentWidth, contentHeight) => {
    this.setState({ screenHeight: contentHeight });
  };

  render() {
    const scrollEnabled = this.state.screenHeight > height;
    return (
      <View style={{ flex: 1, justifyContent: 'flex-start' }}>
        <ScrollView
          style={{ flex: 1 }}
          scrollEnabled={scrollEnabled}
          onContentSizeChange={this.onContentSizeChange}
          contentContainerStyle={{ flexGrow: 1}}
          showsVerticalScrollIndicator={false}>

          <View style={styles.vacationInfo}>
            <VacationInfo/>
          </View>
          <View style={styles.vacationList}>
            <View style={styles.listHeader}>
              <Button title="+"/>
            </View>
            <VacationList/>
          </View>
          <View style={styles.vacationType}>
            <VacationType/>
          </View>
          
        </ScrollView>
      </View>
    )
  }
}



const styles = StyleSheet.create({
  vacationList: {
    flex: 1,
    marginRight: 20,
  },

  listHeader: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
  },

  vacationInfo: {
    height: 180,
    marginBottom: 20,
  },

  vacationType: {
    flex: 1,
  },
})