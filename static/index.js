var fileName;
$(document).ready(function () {
  $("#inpainted-music a ").click(function () {
    // switch to the selected model
    const songNumber = $(this).parent().parent().attr("id");
    const midiUrl = $(this).attr("midi-url");
    const midiPlayerId = songNumber + "-" + "player";
    const midiVisualizerId = songNumber + "-" + "visualizer";
    $("#" + midiPlayerId).attr("src", midiUrl);
    $("#" + midiVisualizerId).attr("src", midiUrl);

    // set the anchor tag selected
    $("#" + songNumber + " a.selected").removeAttr("class");
    $(this).attr("class", "selected");
  });
  $("#try a").click(function () {
    // switch to the selected model
    const songNumber = $(this).parent().parent().parent().attr("id");
    const midiUrl = $(this).attr("midi-url");
    const midiPlayerId = songNumber + "-" + "player";
    const midiVisualizerId = songNumber + "-" + "visualizer";
    $("#" + midiPlayerId).attr("src", midiUrl);
    $("#" + midiVisualizerId).attr("src", midiUrl);

    // set the anchor tag selected
    $("#" + songNumber + " a.selected").removeAttr("class");
    $(this).attr("class", "selected");
  });
});
$(document).ready(function () {
  $("#file-upload").change(function (e) {
    fileName = e.target.files[0].name;
    $("#file-name").text("MIDI File has been selected:  " + fileName);
    $(".displayer").hide();
  });
});

$(document).ready(function () {
  $("#upload-midi").click(function (e) {
    e.preventDefault();
    $(".displayer").hide();
    var formData = new FormData($("#upload-form")[0]);
    if (fileName != undefined) {
      $("#loading-midi").show();
    }
    $.ajax({
      url: "/upload",
      type: "POST",
      data: formData,
      contentType: false,
      cache: false,
      processData: false,
      success: function (response) {
        $(".displayer").show();
        $("#file-name2").text(
          "Your MIDI File has been successfully uploaded: " + fileName
        );
        $("#melody").attr("midi-url", response.message);
        $("#try-song1-visualizer,#try-song1-player").attr(
          "src",
          response.message
        );
        $("#loading-midi").hide();
        $("#accompaniment").hide();
      },
      error: function (jqXHR, textStatus, errorMessage) {
        console.log(errorMessage);
      },
    });
  });
});
$(document).ready(function () {
  $("#generate-midi").click(function (e) {
    $("#generating-midi").show();
    $.ajax({
      url: "/generate",
      type: "POST",
      data: fileName,
      contentType: false,
      cache: false,
      processData: false,
      success: function (response) {
        $("#generating-midi").hide();
        $("#accompaniment").attr("midi-url", response.message);
        $("#try-song1-visualizer,#try-song1-player").attr(
          "src",
          response.message
        );
        $("#accompaniment").attr("class", "selected");
        $("#melody").removeAttr("class");
        $("#accompaniment").show();
        $("#download-midi").show();
      },
      error: function (jqXHR, textStatus, errorMessage) {
        console.log(errorMessage);
      },
    });
  });
});
$(document).ready(function () {
  $("#download-midi-button").click(function () {
    window.location.href = $("#accompaniment").attr("midi-url");
  });
});
