
jQuery(document).ready(function(){
    $('.selectpicker').selectpicker();

    if( /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
        $('.selectpicker').selectpicker('mobile');
    }
});

var current_pagination = 0;

function set_current_page(pg){
    current_pagination = pg;
}

function sc_inc(){
    current_pagination = current_pagination + 1;
}

function sc_dec(){
    current_pagination = current_pagination - 1;
}

function filter_search(){
    var selected_categories = $("select[name='categories']").val();
    var selected_release_years = $("select[name='release_years']").val();
    var selected_production_companies = $("select[name='production_companies']").val();
    var keyword = $("input[name='keyword']").val();
    var only_subtitled = $("#only_sb_option").is(":checked");
    var order_type = $("#order_type").val();
    var only_unlisted = $("#only_unlisted").is(":checked");

    var url = "/?filter=true" +
            (selected_categories ? "&genre=" + selected_categories.join(",") : "") +
            (selected_release_years ? "&years=" + selected_release_years.join(",") : "") +
            (selected_production_companies ? "&companies=" + selected_production_companies.join(",") : "") +
            (keyword ? "&keyword=" + encodeURIComponent(keyword) : "" ) +
            "&order=" + (order_type ? order_type : "standard") +
            "&sb=" + only_subtitled + "&ou=" + only_unlisted + "&page=" + current_pagination;

    url = (location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '')) + url;
    window.location = url;
}