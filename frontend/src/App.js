import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import './stylesheets/App.css';
import FormView from './components/FormView';
import QuestionView from './components/QuestionView';
import Header from './components/Header';
import QuizView from './components/QuizView';
import Login from './components/Login';
import SignUp from './components/SignUp';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      loggedIn: false,
      userDetails: null,
    };
  }

  setUserDetails(data) {
    const { username, score, token } = data;
    const details = {
      username,
      score,
      token,
    };
    this.setState({ loggedIn: true, userDetails: details });
  }

  render() {
    console.log('log in app', this.state.loggedIn);
    return (
      <div className='App'>
        <Header
          path
          loggedIn={this.state.loggedIn}
          userDetails={this.state.userDetails}
        />
        <Router>
          <Switch>
            <Route path='/' exact component={QuestionView} />
            <Route path='/add' component={FormView} />
            <Route path='/play' component={QuizView} />
            <Route
              path='/login'
              component={() => (
                <Login
                  loggedIn={this.state.loggedIn}
                  setUserDetails={(data) => this.setUserDetails(data)}
                />
              )}
            />
            <Route
              path='/signup'
              component={() => (
                <SignUp
                  loggedIn={this.state.loggedIn}
                  setUserDetails={(data) => this.setUserDetails(data)}
                />
              )}
            />
            <Route component={QuestionView} />
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
