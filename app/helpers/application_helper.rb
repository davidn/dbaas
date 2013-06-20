module ApplicationHelper

	def validation_class(obj, class_name)
		class_name unless obj.new_record?
	end
  
  def return_active_class(link_name, current_step)
    if current_step == "confirmation" && (link_name == "management"|| link_name == "basic")
      debugger
      return "complete"
    elsif (current_step == "management" && link_name == "basic" && link_name != "management" && link_name != "confirmation")
      return "complete"
    elsif link_name == current_step
      return "selected"
    end
  end

end