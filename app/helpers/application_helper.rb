module ApplicationHelper

	def validation_class(obj, class_name)
		class_name unless obj.new_record?
	end
  
  def return_active_class(link_name, current_step)
    if link_name == current_step
      return "selected"
    end
    
  end
  

end
