import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import SanpbioAppBar from './components/SnapbioAppBar';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';


const styles = theme => ({
  root: {
    flexGrow: 1,
  },
  form: {
    marginLeft: '2rem',
  },
  paper: {
    padding: theme.spacing.unit * 2,
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
  header: {
    textAlign: 'left'
  },
  card: {
    textAligh: 'left'
  },
  cardContent: {
    textAligh: 'left'
  },
  media: {
    height: 140,
    paddingTop: '56.25%', // 16:9
  },
  fieldTitle: {
    fontWeight: 700,
    marginRight: '0.5rem'
  }
  
});

class ReportDetailPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      name: 'Disease',
      probability: 92,
      description: '',
      imageUrl: 'https://material-ui.com/static/images/cards/contemplative-reptile.jpg',
      lon: 0,
      lat: 0,
      zipCode: '0000',
      open: false,
      sendZipRange: 0,
      sendZipCode: '',
      loaded: false,
      error: null,
    }
  }

  handleClickOpen = () => {
    this.setState({ open: true });
  };

  componentDidMount() {
    const {match} = this.props;

    fetch('/mpi/incident/' + match.params.id)
      .then((result) => result.json())
      .then(
      (result) => {
        this.setState({
          name: result.name,
          probability: parseFloat(result.probability) * 100,
          description: result.description,
          imageUrl: result.photoUrl,
          lon: result.lat,
          lat: result.lon,
          zipCode: result.zipcode,
          open: false,
          sendZipRange: 0,
          sendZipCode: '',
          loaded: true
        });
      },
        (error) => {
          this.setState({error: error, loaded: false});
        }
      );
  }

  handleClose = () => {
    this.setState({ open: false });
  };
  
  handleSendAlert = () => {

    console.log('zip state:', this.state.sendZipCode);
    console.log('zip range state:', this.state.sendZipRange);
    
    this.handleClose();

    //todo: will call api and pass the zip code and range
    // ajax call send this.state.sendZipRange and this.state.sendZipCode
  }

  handleSendZipChange = (event) => {
    this.setState({
      sendZipCode: event.target.value
    })

    console.log('zip value: ', event.target.value)
    console.log('zip state:', this.state.sendZipCode);
  }

  handleSendZipRangeChange = (event) => {
    this.setState({
      sendZipRange: event.target.value
    })

    console.log('zip range value: ', event.target.value)
    console.log('zip range state:', this.state.sendZipRange);
  }

  getDialog() {
    return (
      <Dialog
          open={this.state.open}
          onClose={this.handleClose}
          aria-labelledby="form-dialog-title"
        >
          <DialogTitle id="form-dialog-title">Send regional alert</DialogTitle>
          <DialogContent>
            <DialogContentText>
              This will send out regional alert base on the zip code and range.
            </DialogContentText>
            <TextField
              autoFocus
              margin="dense"
              id="zipcode"
              label="Zip Code"
              type="text"
              value={this.state.sendZipCode}
              onChange={this.handleSendZipChange}
            />
            <br/>
            <TextField
              autoFocus
              margin="dense"
              id="range"
              label="Range (km)"
              type="number"
              value={this.state.sendZipRange}
              onChange={this.handleSendZipRangeChange}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleClose} color="primary">
              Cancel
            </Button>
            <Button onClick={this.handleSendAlert} color="primary">
              send
            </Button>
          </DialogActions>
        </Dialog>
    )
  }


  getForm() {
    const {classes} = this.props;
    return (
      <Card className={classes.card}>
        <CardMedia
          className={classes.media}
          image={this.state.imageUrl}
          title="Contemplative Reptile"
        />
        <CardContent className={classes.cardContent}>
          <Typography gutterBottom variant="headline" component="h2">
            {this.state.name}
          </Typography>
          <Typography component="p">
            <span className={classes.fieldTitle}>Probability</span>
            <span className={classes.field}>{this.state.probability + '%'}</span>
          </Typography>
          <Typography component="p">
            <span className={classes.fieldTitle}>Longitude</span>
            <span className={classes.field}>{this.state.lon}</span>
          </Typography>
          <Typography component="p">
            <span className={classes.fieldTitle}>Latitude</span>
            <span className={classes.field}>{this.state.lat}</span>
          </Typography>
          <Typography component="p">
            <span className={classes.fieldTitle}>Zip Code</span>
            <span className={classes.field}>{this.state.zipCode}</span>
          </Typography>
        </CardContent>
        <CardActions>
          {/* <Button size="small" color="primary">
            Share
          </Button> */}
          <Button size="small" color="primary" onClick={this.handleClickOpen}>
            Alert
          </Button>
        </CardActions>
      </Card>
    )
  }

  render() {
    const {match, classes} = this.props;
    const {error, loaded} = this.state;
    if (error) {
      return <div>Error</div>
    } else if (!loaded) {
      return <div>loading...</div>
    } else {
      // {match.params.id}
      return (
        <div className={classes.root}>
          <Grid container spacing={24}>
            <Grid className={classes.header} item xs={12}>
              <SanpbioAppBar title={'Report ' + this.state.name}/>
            </Grid>
            <Grid item sm={12} md= {10} lg={5} className={classes.form} >
                {this.getForm()}
            </Grid>
          </Grid>
          {this.getDialog()}
        </div>
      )
    }
  }
}

export default withStyles(styles)(ReportDetailPage)