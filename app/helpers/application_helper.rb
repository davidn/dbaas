module ApplicationHelper

	def validation_class(obj, class_name)
		class_name unless obj.new_record?
	end
  
  def return_active_class(current_step)
    
  end
  

end
