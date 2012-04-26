$(document).ready(function(){
    $('a',$('.list_filter')).each(function(){
        var t_url = $(this).parent().parent().attr('ajax_url');
        var t_filter_name = $(this).parent().parent().attr('t_filter_name');
        var t_filter_value = $(this).attr('t_filter_value');
        if(t_filter_value){
            var tparam = {};
            tparam['t_filter']=true;
            tparam['t_filter_name']=t_filter_name;
            tparam['t_filter_value']=t_filter_value;
            t_url= $.param.querystring(t_url, tparam);
            $(this).attr('href',t_url);
        }
    });
});