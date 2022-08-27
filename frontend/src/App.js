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
  render() {
    return (
      <div className='App'>
        <Header path />
        <Router>
          <Switch>
            <Route path='/' exact component={QuestionView} />
            <Route path='/add' component={FormView} />
            <Route path='/play' component={QuizView} />
            <Route path='/login' component={Login} />
            <Route path='/signup' component={SignUp} />
            <Route component={QuestionView} />
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
