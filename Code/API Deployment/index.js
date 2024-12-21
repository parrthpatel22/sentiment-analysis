
Chart.defaults.global.defaultFontSize = 16;


var data = {"word": "ronaldo"};
var json_data = JSON.stringify(data);



function randomColor() {
    var x = Math.floor(Math.random() * 256);
    var y = Math.floor(Math.random() * 256);
    var z = Math.floor(Math.random() * 256);
	return {x: x, y: y, z:z}
	
    }


$(document).ready(function(){
	
$(".load").hide();	
$(".loader").hide();	
  
$("#submit").click(function(){
	console.log('hello');
	var string = $("#words").val();
	var words = string.split(",");
	var data = {words: words};
	var json_data = JSON.stringify(data);
	console.log(json_data);
	$(".load").show();
	$(".loader").show();	

	$.ajax({
    type: 'POST',
    url: 'https://bfb2-115-96-216-213.in.ngrok.io/sentiments',
    data: json_data, // or JSON.stringify ({name: 'jonas'}),
    success: function(response) { 
	
		$(".load").hide();
		$(".loader").hide();	

		console.log(response);
		var fill_datasets = [];
		var no_fill_datasets = [];
		var colors = [];
		var bgcolors = [];
		var posTotal = [];
		for(var i = 0;i<7;i++)
		{
			var values = randomColor();
			var bgColor = "rgb(" + values.x + "," + values.y + "," + values.z + ")";
			var bColor = "rgb(" + values.x + "," + values.y + "," + values.z + ",0.2)";
			colors.push(bgColor);
			bgcolors.push(bColor);
		}
		for(var count = 0; count<words.length;count++)
		{
			var labels = [];
			var positive = [];
			var negative = [];
			for(var i = 6;i>-1;i--)
			{
				d = new Date();
				d.setDate(d.getDate() - i);
				labels.push(d.toISOString().slice(0, 10));
			}
			var total = 0;
			for(var i = 6;i>-1;i--)
			{
			d = new Date();
			d.setDate(d.getDate() - i);
			console.log(d.toISOString().slice(0, 10));
			positive.push(response[words[count]][d.toISOString().slice(0, 10)]['pos_count']);
			negative.push(response[words[count]][d.toISOString().slice(0, 10)]['neg_count']);
			console.log(response[words[count]][d.toISOString().slice(0, 10)]);	
			total = total + response[words[count]][d.toISOString().slice(0, 10)]['pos_count'];
			}
			no_fill_datasets.push({data: positive, label: words[count], borderColor: colors[count],fill: false});
			
			fill_datasets.push({data: positive, label: words[count], borderColor: colors[count],fill: true, backgroundColor: bgcolors[count] });
			posTotal.push(total);
		}
		
		
		
		var barChartLoc = document.getElementById('barChartLoc');
		barChartLoc.innerHTML = "<canvas id='bar-chart' width='10' height='8'></canvas>";
		
		var lineChartLoc = document.getElementById('lineChartLoc');
		lineChartLoc.innerHTML = "<canvas id='lineChart' width='10' height='8' style='padding-top: 1%;'></canvas>"   ;
		
		var radarChartLoc = document.getElementById('radarChartLoc');
		radarChartLoc.innerHTML = "<canvas id='radar-chart' width='10' height='8'></canvas>";
		
		var doughnutChartLoc = document.getElementById('doughnutChartLoc');
		doughnutChartLoc.innerHTML = "<canvas id='doughnut-chart' width='10' height='8'></canvas>";
		
		
		new Chart(document.getElementById("lineChart"), {
    type: 'line',
    data: {
      labels: labels,
      datasets: no_fill_datasets
    },
    options: {
      title: {
        display : true,
      position : "top",
      fontSize : 24,
      fontColor : "#111",
        text: "Positive Tweets"
      },
        
        legend:{
            display:true
        }
    }
  });



new Chart(document.getElementById("radar-chart"), {
  type: 'radar',
  data: {
    labels: labels,
    datasets: fill_datasets
  },
  options: {
    title: {
      display : true,
      position : "top",
      fontSize : 24,
      fontColor : "#111",
      text: 'Positive Tweets'
    },scale: {
      ticks: {
          beginAtZero: true,
          stepSize: 20,
		  fontSize: 10
      }
  }
  }
});




var ctx = $("#bar-chart");

  var data = {
    labels : labels,
    datasets : fill_datasets
  };

  var options = {
    title : {
      text : "Word-Wise Classification",
      display : true,
      position : "top",
      fontSize : 24,
      fontColor : "#111"
    },
    legend : {
      display : true
    },
    scales : {
      yAxes : [{
        ticks : {
          min : 0
        }
      }]
    }
  };

  var chart = new Chart( ctx, {
    type : "bar",
    data : data,
    options : options
  });
  new Chart(document.getElementById("doughnut-chart"), {
    type: 'doughnut',
    data: {
      labels: words,
      datasets: [
        {
          label: "Tweets",
		  borderColor: colors,
          backgroundColor: bgcolors,
          data: posTotal
        }
      ]
    },
    options: {
      title: {
        display : true,
      position : "top",
      fontSize : 24,
      fontColor : "#111",
        text: 'Cumulative Tweets Analysis'
      }
    }
});









	},
    contentType: "application/json",
    dataType: 'json'
});





	
	
});


	




    
  
  
  
});

