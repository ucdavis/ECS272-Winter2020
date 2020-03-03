import * as moment from 'moment'

function getDates(startDate, stopDate) {
    var dateArray = [];
    var currentDate = moment(startDate);
    var endDate = moment(stopDate);
    while (currentDate <= endDate) {
        dateArray.push(moment(currentDate).format('M/D/YY'))
        currentDate = moment(currentDate).add(1, 'days');
    }
    return dateArray;
}

export default getDates