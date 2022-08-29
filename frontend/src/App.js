import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import './stylesheets/App.css';
import FormView from './components/FormView';
import QuestionView from './components/QuestionView';
import Header from './components/Header';
import QuizView from './components/QuizView';
import Login from './components/Login';
import SignUp from './components/SignUp';
import Profile from './components/Profile';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      loggedIn: false,
      userDetails: null,
    };
  }

  componentDidMount() {
    let loggedIn = localStorage.getItem('loggedIn');
    if (loggedIn === 'false') {
      loggedIn = false;
    }
    const details = localStorage.getItem('userDetails');
    this.setState({ loggedIn, userDetails: JSON.parse(details) });
  }

  setUserDetails(data, loggedIn) {
    const { username, score, token } = data;
    const details = {
      username,
      score,
      token,
    };
    console.log('token', token);
    this.setState({ loggedIn, userDetails: details });
    localStorage.setItem('loggedIn', loggedIn);
    localStorage.setItem('userDetails', JSON.stringify(details));
  }

  render() {
    const { loggedIn, userDetails } = this.state;
    return (
      <div className='App'>
        <Header
          path
          loggedIn={loggedIn}
          userDetails={userDetails}
          setUserDetails={(data, loggedIn) =>
            this.setUserDetails(data, loggedIn)
          }
        />
        <Router>
          <Switch>
            <Route path='/' exact component={QuestionView} />
            <Route path='/add' component={FormView} />
            <Route
              path='/profile'
              component={() => (
                <Profile userDetails={userDetails} loggedIn={loggedIn} />
              )}
            />
            <Route
              path='/play'
              component={() => (
                <QuizView
                  loggedIn={loggedIn}
                  userDetails={userDetails}
                  setUserDetails={(data, loggedIn) =>
                    this.setUserDetails(data, loggedIn)
                  }
                />
              )}
            />
            <Route
              path='/login'
              component={() => (
                <Login
                  loggedIn={loggedIn}
                  setUserDetails={(data, loggedIn) =>
                    this.setUserDetails(data, loggedIn)
                  }
                />
              )}
            />
            <Route
              path='/signup'
              component={() => (
                <SignUp
                  loggedIn={loggedIn}
                  setUserDetails={(data, loggedIn) =>
                    this.setUserDetails(data, loggedIn)
                  }
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
