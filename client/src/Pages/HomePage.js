import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Avatar from '@material-ui/core/Avatar';
import ImageIcon from '@material-ui/icons/Image';
import WorkIcon from '@material-ui/icons/Work';
import BeachAccessIcon from '@material-ui/icons/BeachAccess';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import SanpbioAppBar from './components/SnapbioAppBar';

const styles = theme => ({
  root: {
  flexGrow: 1,
  },
  listcontainer: {
  width: '100%',
  // maxWidth: 1080,
  backgroundColor: theme.palette.background.paper,
  },
  paper: {
  padding: theme.spacing.unit * 2,
  textAlign: 'center',
  color: theme.palette.text.secondary,
  },
  header: {
    textAlign: 'left'
  }
});

class HomePage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      reportedItems: [],
      loaded: false,
      error: null,
    }
  }

  componentDidMount() {
    fetch('/mpi/incidents')
      .then((result) => result.json())
      .then(
      (result) => {
        this.setState({
          reportedItems: result.incidents,
          loaded: true,
        });
      },
      (error) => {
        this.setState({error: error, loaded: false});
      }
      );
  }

  createList(){
    const {classes, history} = this.props;
    return (
      <div className={classes.listcontainer}>
        <List>
          {this.state.reportedItems.map((incident) => (
            <ListItem key={incident.id} button onClick={() => history.push('report/' + incident.id)}>
              <Avatar style={{backgroundColor:'#FF6F00'}}>
                <ImageIcon />
              </Avatar>
              <ListItemText primary={incident.name} secondary={incident.timestamp} />
            </ListItem>
          ))}
        </List>
      </div>
    )
  }

  render() {
    const {classes} = this.props;
    const {reportedItems, error, loaded} = this.state;
    if (error) {
      return <div>Error</div>
    } else if (!loaded) {
      return <div>loading...</div>
    } else {
      return (
        <div className={classes.root}>
      <Grid container justify="center" spacing={24}>
            <Grid className={classes.header} item xs={12}>
              <SanpbioAppBar title="Home"/>
            </Grid>
        <Grid item xs={10}>
              <Paper className={classes.paper}>
                {this.createList()}
              </Paper>
            </Grid>
          </Grid>
        </div>
      )
    }
  }
}

export default withStyles(styles)(HomePage)