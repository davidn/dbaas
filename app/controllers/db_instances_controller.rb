class DbInstancesController < ApplicationController

	def index
		if session[:db_params]
			@db_instance = DbInstance.new(session[:db_params])
			@db_instance.current_step = session[:db_step]
			render :new
		else
			reset_session
			session[:db_params] ||= {}
			@db_instance = DbInstance.new
			render :new
		end
	end

	def new
		reset_session
		session[:db_params] ||= {}
		@db_instance = DbInstance.new
	end

	def create
		if session[:db_params]
			session[:db_params].deep_merge!(params[:db_instance]) if params[:db_instance]
			@db_instance = DbInstance.new(session[:db_params])
			@db_instance.current_step = session[:db_step]
			if @db_instance.valid?
				if params[:db_instance] and params[:db_instance]["backup_window"] == "no_preference"
					@db_instance.daily_backup_duration = params[:db_instance]["daily_backup_duration"] = session[:db_params]["daily_backup_duration"] = nil rescue nil
					@db_instance.daily_backup_start_time = params[:db_instance]["daily_backup_start_time"] = session[:db_params]["daily_backup_start_time"] = nil rescue nil
				end
				if params[:back_button]
					@db_instance.previous_step
				elsif @db_instance.last_step?
					@db_instance.launch
					@db_instance.save
				else
					@db_instance.next_step
				end
			end
			session[:db_step] = @db_instance.current_step
			if @db_instance.new_record?
				render "new"
			else
				session[:db_params] = session[:db_step] = nil
				flash[:notice] = "Instance Saved"
				render "thanks"
			end
		else
			redirect_to new_db_instance_path
		end
	end

	def show
		@db_instance = DbInstance.find(params[:id])
	end

end
